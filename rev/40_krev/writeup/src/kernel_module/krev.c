#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/ioctl.h>
#include <linux/kprobes.h>
#include <crypto/internal/hash.h>
#include <crypto/md5.h>

#include <asm/uaccess.h>

#define DEVICE_NAME "krev"
#define DEVICE_CLASS_NAME "krev_dev"

// define commands
#define IOCTL_BASE 'W'
#define	CMD_UNLOCK	_IO(IOCTL_BASE, 0)
#define	CMD_WRITE	_IO(IOCTL_BASE, 1)

static struct class *krev_class;
static int major_num;
static struct file_operations file_ops;
static unsigned long (*my_kallsyms_lookup_name)(const char *name);
static void *my_modprobe_path = NULL;
static bool locked = true;

// https://nskernel.gitbook.io/kernel-play-guide/accessing-the-non-exported-in-modules
static void *lookup_kallsyms_lookup_name(void)
{
    struct kprobe kp;
    unsigned long addr;

    memset(&kp, 0, sizeof(struct kprobe));
    kp.symbol_name = "kallsyms_lookup_name";
    if (register_kprobe(&kp) < 0) {
        return 0;
    }
    addr = (unsigned long)kp.addr;
    unregister_kprobe(&kp);
    return (void *)addr;
}

static int krev_open(struct inode *inode, struct file *file)
{
	printk(KERN_INFO "vulnerable device is opened\n");
	return 0;
}

static int krev_release(struct inode *inode, struct file *file)
{
	printk(KERN_INFO "vulnerable device is closed\n");
	return 0;
}

const char ans2[] = "\xcb\x05\x4f\x37\xb5\xb2\x6d\x39\x54\xc2\x1d\xfb\x5b\xe4\x32\x77";

static int verify(void *inp)
{
	char *inp1 = inp;
	char *inp2 = inp+0x10;
	void *inp3 = inp+0x20;
	void *inp4 = inp+0x30;
	//void *inp5 = inp+0x40;

	// input 1
	if(strncmp(inp1, "CUHK", 4)) {
		printk(KERN_INFO "0ops!\n");
		return 0;
	}

	// input 2
	char prev = 0x41;
	bool good = true;
	for(int i=0; i<0x10; i++) {
		prev = inp2[i]^prev;
		// printk("i: %d, prev: %#x\n", i, prev);
		if(prev != ans2[i]) {
			good = false;
			break;
		}
	}
	if (!good) {
		printk(KERN_INFO "00ops!\n");
		return 0;
	}

	// input 3
	u64 tmp = *(u64*)inp3;
	if(tmp * 0xeff0b7f3 != 0x9ab1c6280e1a844e) {
		printk(KERN_INFO "000ops!\n");
		return 0;
	}

	// input 4
	struct crypto_shash *tfm = crypto_alloc_shash("md5", 0, 0);
	if (IS_ERR(tfm)) {
	    return -ENOMEM;
	}
	struct shash_desc *shash = kmalloc(sizeof(struct shash_desc) + crypto_shash_descsize(tfm), GFP_KERNEL);
	if (!shash) {
	    crypto_free_shash(tfm);
	    return -ENOMEM;
	}
	shash->tfm = tfm;

	char out[16];
	crypto_shash_init(shash);
	crypto_shash_update(shash, inp4, 4);
	crypto_shash_final(shash, out);
	if (memcmp(out, "\xa0\x77\xf1\x1a\xfd\xad\x48\x9e\x2e\x06\x23\x2b\x13\x6f\x5a\x83", 16)) {
		printk(KERN_INFO "0000ops!\n");
		return 0;
	}

	return 1;
}

static long krev_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
	//printk(KERN_INFO "krev_ioctl called with cmd: %d, arg: 0x%lx\n", cmd, arg);
	printk(KERN_INFO "krev_ioctl\n");

	switch(cmd) {
		case CMD_UNLOCK:
			char input[0x40];
			memset(input, 0, sizeof(input));

			if (copy_from_user(input, (void *)arg, sizeof(input))) {
				return -EINVAL;
			}
			if (verify(input)) {
				locked = false;
				printk(KERN_INFO "Device unlocked!\n");
				return 0;
			}
			printk(KERN_INFO "Device still locked :)\n");
			return -EINVAL;
		case CMD_WRITE:
			if (locked) {
				printk(KERN_INFO "You need to unlock the device first. Hack harder :)\n");
				return -EINVAL;
			}
			return copy_from_user(my_modprobe_path, (void *)arg, 0x10);
		default:
			return -EINVAL;
	}

	return -EINVAL;
}

static struct file_operations file_ops = { 
	.unlocked_ioctl = krev_ioctl,
	.open = krev_open,
	.release = krev_release
};


/***************************************
 * 
 * kernel module related code
 *
 **************************************/
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Yihui Zeng; zengyhkyle@gmail.com");
MODULE_DESCRIPTION("A vulnerable Linux kernel module for CUHK CTF 2024.");
MODULE_VERSION("0.01");

static int __init krev_init(void)
{
	printk(KERN_INFO "krev module init\n");

	// resolve kallsyms_lookup_name
	my_kallsyms_lookup_name = lookup_kallsyms_lookup_name();
    if (my_kallsyms_lookup_name == NULL) {
        printk(KERN_ERR "fail to find kallsyms_lookup_name...");
        return -EINVAL;
    }
	my_modprobe_path = (void*)my_kallsyms_lookup_name("modprobe_path");
    if (my_modprobe_path == NULL) {
        printk(KERN_ERR "fail to find modprobe_path...");
        return -EINVAL;
    }

	// this registers 0x100 minor numbers
	major_num = register_chrdev(0, DEVICE_NAME, &file_ops);
	if(major_num < 0) {
		printk(KERN_WARNING "Fail to get major number");
		return -EINVAL;
	}

	/* populate a device node */
	krev_class = class_create(DEVICE_CLASS_NAME);
	device_create(krev_class, NULL, MKDEV(major_num, 0), NULL, DEVICE_NAME);

	return 0;
}

static void __exit krev_exit(void)
{
	printk(KERN_INFO "krev module exit\n");

	// destory the device node first
	device_destroy(krev_class, MKDEV(major_num, 0));

	// destroy the device class
	class_destroy(krev_class);

	// unregister chrdev
	unregister_chrdev(major_num, DEVICE_NAME);
}

module_init(krev_init);
module_exit(krev_exit);
