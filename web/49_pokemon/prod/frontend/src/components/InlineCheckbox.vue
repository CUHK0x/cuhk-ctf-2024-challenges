<template>
    <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" :checked="toggle" @change="toggleValue()" :value="name"
            :id="`${id}Check`">
        <label class="form-check-label" :for="`${id}InlineCheckbox`">
            {{ name }}
        </label>
    </div>
</template>

<script>
export default {
    props: ['id', 'name'],
    methods: {
        async toggleValue() {
            this.toggle ^= true;
            this.$parent.fetched = false;
            if (this.toggle) {
                this.$parent.compares.push(this.id);
            } else {
                this.$parent.compares.splice(this.$parent.compares.indexOf(this.id), 1);
            }
            this.$parent.compares.sort((x, y) => {
                var hardcode = {
                    "abilities": 0,
                    "hp": 1,
                    "attack": 2,
                    "defense": 3,
                    "spattack": 4,
                    "spdefense": 5,
                    "speed": 6
                }
                if (hardcode[x] < hardcode[y]) {
                    return -1;
                } else if (hardcode[x] > hardcode[y]) {
                    return 1;
                }
                return 0;
            });
        }
    },
    data() {
        return {
            toggle: false
        }
    }
}
</script>