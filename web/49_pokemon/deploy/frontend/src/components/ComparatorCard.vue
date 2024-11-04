<template>
    <div class="card">
        <div class="card-header">
            <div class="row justify-content-between align-items-center">
                <div class="col-auto">
                    <h5> Pokemon Comparator #{{ index }} </h5>
                </div>
                <div class="col-auto">
                    <input type="pokemonName" v-model="pokemonInput" class="form-control" id="pokemonInput"
                        placeholder="Pokemon Name">
                </div>
                <div class="col-auto">
                    <button type="button" class="btn btn-light bg-transparent text-center"
                        @click.prevent="addNewPokemon()">
                        <div class="d-flex justify-content-center">
                            <h5>Add new Pokemon</h5>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-plus-circle" viewBox="0 0 16 16">
                                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                                <path
                                    d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4" />
                            </svg>
                        </div>
                    </button>
                </div>
                <div class="col-auto">
                    <button type="button" class="btn btn-primary" @click.prevent="submitRequest()"> Compare! </button>
                </div>
            </div>
        </div>
        <!-- Pokemons -->
        <div class="card-body">
            <div class="container-fluid">
                <div class="row row-cols-auto g-2 g-lg-3">
                    <div class="col" v-for="(pokemon, index) in pokemons">
                        <div class="card" style="width: 18rem;">
                            <div class="card-header text-center">
                                <div class="row row-cols-auto justify-content-between align-items-center">
                                    <div class="col" :class="pokemonNameClass(fetchedResult[`_${index + 1}`])">
                                        <h5> {{ pokemon }} </h5>
                                    </div>
                                    <div v-if="fetched && fetchedResult[`_${index + 1}`] != null"
                                        class="col text-secondary">
                                        <small> (#{{ fetchedResult[`_${index + 1}`]["id"] }}) </small>
                                    </div>
                                    <div class="col">
                                        <a href="#" @click.prevent="removePokemon(pokemon)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                                                <path
                                                    d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708" />
                                            </svg>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col text-center">
                                    <img v-if="fetched && fetchedResult[`_${index + 1}`] != null" class="img-fluid"
                                        :src="`/api/image?id=${fetchedResult['_' + (index + 1).toString()]['id'].toString().padStart(3, '0')}`">
                                </div>
                            </div>
                            <div class="card-body">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th scope="col">
                                                Stats
                                            </th>
                                            <th scope="col">
                                                Value
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="col">
                                            <th scope="row"> Type </th>
                                            <td v-if="!fetched || fetchedResult[`_${index + 1}`] == null"> ??? </td>
                                            <td v-if="fetched && fetchedResult[`_${index + 1}`] != null">
                                                <img class="img-fluid"
                                                    :src="`/types/${fetchedResult['_' + (index + 1).toString()]['type1'].toLowerCase()}.gif`">
                                                <span v-if="fetchedResult[`_${index + 1}`]['type2'] != null"> &nbsp; </span>
                                                <img v-if="fetchedResult[`_${index + 1}`]['type2'] != null"
                                                    class="img-fluid"
                                                    :src="`/types/${fetchedResult['_' + (index + 1).toString()]['type2'].toLowerCase()}.gif`">
                                            </td>
                                        </tr>
                                        <tr v-for="comp in compares">
                                            <th scope="row"> {{ statsFullname[comp] }} </th>
                                            <td v-if="!fetched || fetchedResult[`_${index + 1}`] == null"> ??? </td>
                                            <td v-if="fetched && fetchedResult[`_${index + 1}`] != null"
                                                :class="pokemonStatsClass(comp, fetchedResult[`_${index + 1}`][comp])">
                                                {{ fetchedResult[`_${index + 1}`][comp] }} </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-footer">
            <div class="form-check form-check-inline" v-for="stat in stats">
                <inline-checkbox :id="stat" :name="statsFullname[stat]"></inline-checkbox>
            </div>
        </div>
    </div>

</template>

<script>
import InlineCheckbox from "./InlineCheckbox.vue";

export default {
    props: ['index'],
    components: {
        InlineCheckbox
    },
    methods: {
        sanitize(name) {
            const pattern = new RegExp("^[\\wé\'.-\\s♀♂:]+$");
            return pattern.test(name);
        },
        properize(name) {
            return name.replace(
                /\w\S*/g,
                text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
            );
        },
        addNewPokemon() {
            this.fetched = false;
            if (!this.sanitize(this.pokemonInput)) {
                alert("Your Pokemon name contains invalid characters!");
                return;
            } else if (this.pokemons.find((x) => x == this.properize(this.pokemonInput)) != undefined) {
                alert("You have entered this Pokemon already!");
                return;
            } else if (this.pokemons.length >= 8) {
                alert("You have entered too much Pokemons!");
                return;
            }
            this.pokemons.push(this.properize(this.pokemonInput));
            this.pokemonInput = "";
        },
        removePokemon(name) {
            this.fetched = false;
            this.pokemons.splice(this.pokemons.indexOf(name), 1);
        },
        async submitRequest() {
            if (this.pokemons.length > 0) {
                var response = await fetch("/api/query", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        pokemons: this.pokemons,
                        compares: ["id", "type1", "type2"].concat(this.compares)
                    })
                }).then((res) => res.json());
                this.fetchedResult = response["data"];
    
                this.fetched = true;
            } else {
                alert("You don't have Pokemons to compare!")
            }
        },
        pokemonNameClass(obj) {
            return {
                'text-danger': this.fetched && obj == null,
                'emphasize': this.fetched && obj == null
            }
        },
        pokemonStatsClass(statName, statVal) {
            // ignore abilities (can't get max from it)
            if (statName == "abilities") {
                return {}
            }
            // calculate highest
            var arr = [];
            for (var i = 1; i <= this.pokemons.length; i++) {
                if (this.fetchedResult[`_${i}`] != null) {
                    arr.push(this.fetchedResult[`_${i}`][statName]);
                }
            }
            var ok = this.fetched && Math.max(...arr) === statVal;
            return {
                'text-primary': ok,
                'fw-bold': ok
            }
        }
    },
    data() {
        return {
            pokemonInput: "",
            pokemons: [],
            compares: [],
            fetched: false,
            fetchedResult: {},
            stats: ["abilities", "hp", "attack", "defense", "spattack", "spdefense", "speed"],
            statsFullname: {
                "abilities": "Abilities",
                "hp": "HP",
                "attack": "Attack",
                "defense": "Defense",
                "spattack": "Sp. Attack",
                "spdefense": "Sp. Defense",
                "speed": "Speed"
            },
            statsCompareToggle: {
                "abilities": false,
                "hp": false,
                "attack": false,
                "defense": false,
                "spattack": false,
                "spdefense": false,
                "speed": false
            }
        }
    }
}
</script>