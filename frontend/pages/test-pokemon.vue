<template>
  <div class="pokemon-container">
    <h1>Pokemon API Test</h1>

    <div class="search-section">
      <input
        v-model="pokemonName"
        @keyup.enter="fetchPokemon"
        type="text"
        placeholder="Enter Pokemon name (e.g., pikachu, charizard)"
        class="pokemon-input"
      />
      <button @click="fetchPokemon" :disabled="loading" class="fetch-btn">
        {{ loading ? "Loading..." : "Fetch Pokemon" }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="pokemon" class="pokemon-card">
      <div class="pokemon-header">
        <h2>{{ pokemon.name }}</h2>
        <span class="pokemon-id">#{{ pokemon.id }}</span>
      </div>

      <div class="pokemon-image">
        <img
          :src="
            pokemon.sprites.other['official-artwork'].front_default ||
            pokemon.sprites.front_default
          "
          :alt="pokemon.name"
        />
      </div>

      <div class="pokemon-info">
        <div class="info-section">
          <h3>Types</h3>
          <div class="types">
            <span
              v-for="type in pokemon.types"
              :key="type.slot"
              class="type-badge"
              :class="`type-${type.type.name}`"
            >
              {{ type.type.name }}
            </span>
          </div>
        </div>

        <div class="info-section">
          <h3>Stats</h3>
          <div class="stats">
            <div
              v-for="stat in pokemon.stats"
              :key="stat.stat.name"
              class="stat-item"
            >
              <span class="stat-name">{{
                formatStatName(stat.stat.name)
              }}</span>
              <div class="stat-bar-container">
                <div
                  class="stat-bar"
                  :style="{ width: `${(stat.base_stat / 255) * 100}%` }"
                ></div>
              </div>
              <span class="stat-value">{{ stat.base_stat }}</span>
            </div>
          </div>
        </div>

        <div class="info-section">
          <h3>Abilities</h3>
          <div class="abilities">
            <span
              v-for="ability in pokemon.abilities"
              :key="ability.slot"
              class="ability-badge"
            >
              {{ ability.ability.name }}
            </span>
          </div>
        </div>

        <div class="info-section">
          <h3>Details</h3>
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Height:</span>
              <span class="detail-value">{{ pokemon.height / 10 }}m</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Weight:</span>
              <span class="detail-value">{{ pokemon.weight / 10 }}kg</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Base Experience:</span>
              <span class="detail-value">{{ pokemon.base_experience }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!pokemon && !loading && !error" class="placeholder">
      <p>Enter a Pokemon name and click "Fetch Pokemon" to get started!</p>
      <p class="suggestions">Try: pikachu, charizard, mewtwo, eevee, lucario</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const { externalApi } = useApi();

const pokemonName = ref("pikachu");
const pokemon = ref<any>(null);
const loading = ref(false);
const error = ref("");

const fetchPokemon = async () => {
  if (!pokemonName.value.trim()) {
    error.value = "Please enter a Pokemon name";
    return;
  }

  loading.value = true;
  error.value = "";
  pokemon.value = null;

  try {
    const response = await externalApi.get(
      `https://pokeapi.co/api/v2/pokemon/${pokemonName.value.toLowerCase()}`
    );
    pokemon.value = response.data;
  } catch (err: any) {
    if (err.response?.status === 404) {
      error.value = `Pokemon "${pokemonName.value}" not found. Please try another name.`;
    } else {
      error.value = "Failed to fetch Pokemon data. Please try again.";
    }
    console.error("Error fetching Pokemon:", err);
  } finally {
    loading.value = false;
  }
};

const formatStatName = (name: string) => {
  return name
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};

// Auto-fetch Pikachu on mount
onMounted(() => {
  fetchPokemon();
});
</script>

<style scoped>
.pokemon-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}

h1 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 2rem;
}

.search-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.pokemon-input {
  flex: 1;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  outline: none;
  transition: all 0.3s ease;
  background: white;
}

.pokemon-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.fetch-btn {
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
}

.fetch-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
}

.fetch-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 1rem 1.25rem;
  background: #fee;
  border-left: 4px solid #f44;
  border-radius: 8px;
  color: #c33;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.pokemon-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.pokemon-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.pokemon-header h2 {
  margin: 0;
  font-size: 2rem;
  text-transform: capitalize;
  font-weight: 700;
}

.pokemon-id {
  font-size: 1.5rem;
  font-weight: 700;
  opacity: 0.9;
}

.pokemon-image {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

.pokemon-image img {
  max-width: 300px;
  height: auto;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.15));
  transition: transform 0.3s ease;
}

.pokemon-image img:hover {
  transform: scale(1.05);
}

.pokemon-info {
  padding: 2rem;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section:last-child {
  margin-bottom: 0;
}

.info-section h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1rem;
}

.types {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.type-badge {
  padding: 0.5rem 1.25rem;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.5px;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Pokemon type colors */
.type-normal {
  background: #a8a878;
}
.type-fire {
  background: #f08030;
}
.type-water {
  background: #6890f0;
}
.type-electric {
  background: #f8d030;
  color: #333;
}
.type-grass {
  background: #78c850;
}
.type-ice {
  background: #98d8d8;
}
.type-fighting {
  background: #c03028;
}
.type-poison {
  background: #a040a0;
}
.type-ground {
  background: #e0c068;
}
.type-flying {
  background: #a890f0;
}
.type-psychic {
  background: #f85888;
}
.type-bug {
  background: #a8b820;
}
.type-rock {
  background: #b8a038;
}
.type-ghost {
  background: #705898;
}
.type-dragon {
  background: #7038f8;
}
.type-dark {
  background: #705848;
}
.type-steel {
  background: #b8b8d0;
}
.type-fairy {
  background: #ee99ac;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: grid;
  grid-template-columns: 140px 1fr 60px;
  gap: 1rem;
  align-items: center;
}

.stat-name {
  font-weight: 600;
  color: #4a5568;
  text-transform: capitalize;
}

.stat-bar-container {
  background: #e2e8f0;
  border-radius: 10px;
  height: 12px;
  overflow: hidden;
}

.stat-bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  transition: width 0.8s ease;
}

.stat-value {
  font-weight: 700;
  color: #2d3748;
  text-align: right;
}

.abilities {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.ability-badge {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border-radius: 12px;
  font-weight: 600;
  text-transform: capitalize;
  font-size: 0.875rem;
  box-shadow: 0 2px 8px rgba(245, 87, 108, 0.3);
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: #f7fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.detail-label {
  font-weight: 600;
  color: #4a5568;
}

.detail-value {
  font-weight: 700;
  color: #2d3748;
}

.placeholder {
  text-align: center;
  padding: 4rem 2rem;
  color: #718096;
}

.placeholder p {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.suggestions {
  font-size: 0.875rem;
  color: #a0aec0;
  font-style: italic;
}
</style>
