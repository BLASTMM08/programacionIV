import collections
import time
from typing import Dict, Iterable, List, Optional, Tuple

import requests


class PokeAPIClient:
    base_url = "https://pokeapi.co/api/v2"

    def __init__(self, max_retries: int = 3, backoff: float = 0.5):
        self.session = requests.Session()
        # Avoid inheriting proxy settings that could block requests in restricted
        # environments.
        self.session.trust_env = False
        self.max_retries = max_retries
        self.backoff = backoff
        self._pokemon_cache: Dict[str, dict] = {}
        self._species_cache: Dict[str, dict] = {}

    def _request_json(self, url: str) -> dict:
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.RequestException:
                if attempt == self.max_retries:
                    raise
                time.sleep(self.backoff * attempt)
        raise RuntimeError("Unexpected request handling state")

    def get_json(self, path: str) -> dict:
        url = path if path.startswith("http") else f"{self.base_url}/{path.strip('/')}"
        return self._request_json(url)

    def paginated_results(self, path: str) -> Iterable[dict]:
        url = f"{self.base_url}/{path.strip('/')}"
        while url:
            payload = self._request_json(url)
            for result in payload.get("results", []):
                yield result
            url = payload.get("next")

    def pokemon(self, name: str) -> dict:
        if name not in self._pokemon_cache:
            self._pokemon_cache[name] = self.get_json(f"pokemon/{name}")
        return self._pokemon_cache[name]

    def species(self, name: str) -> dict:
        if name not in self._species_cache:
            self._species_cache[name] = self.get_json(f"pokemon-species/{name}")
        return self._species_cache[name]


def get_type_pokemon(client: PokeAPIClient, type_name: str) -> List[str]:
    data = client.get_json(f"type/{type_name}")
    return [entry["pokemon"]["name"] for entry in data.get("pokemon", [])]


def get_default_pokemon_for_species(client: PokeAPIClient, species_data: dict) -> Optional[dict]:
    for variety in species_data.get("varieties", []):
        if variety.get("is_default"):
            return client.pokemon(variety["pokemon"]["name"])
    return None


def flatten_evolution_chain(chain: dict) -> List[str]:
    sequence = []
    node_queue = [chain]
    while node_queue:
        node = node_queue.pop(0)
        sequence.append(node["species"]["name"])
        node_queue.extend(node.get("evolves_to", []))
    return sequence


def fire_pokemon_in_kanto(client: PokeAPIClient) -> int:
    species_seen = set()
    count = 0
    for pokemon_name in get_type_pokemon(client, "fire"):
        species_data = client.species(pokemon_name)
        species_name = species_data["name"]
        if species_name in species_seen:
            continue
        species_seen.add(species_name)
        if species_data.get("generation", {}).get("name") == "generation-i":
            count += 1
    return count


def tall_water_pokemon(client: PokeAPIClient, min_height: int = 11) -> List[str]:
    names = []
    seen = set()
    for pokemon_name in get_type_pokemon(client, "water"):
        if pokemon_name in seen:
            continue
        seen.add(pokemon_name)
        pokemon_data = client.pokemon(pokemon_name)
        if pokemon_data.get("height", 0) >= min_height:
            names.append(pokemon_data["name"])
    return sorted(names)


def evolution_chain_for_starter(client: PokeAPIClient, starter: str) -> List[str]:
    species_data = client.species(starter)
    chain_url = species_data.get("evolution_chain", {}).get("url")
    if not chain_url:
        return [starter]
    chain_data = client.get_json(chain_url)
    return flatten_evolution_chain(chain_data["chain"])


def electric_without_evolutions(client: PokeAPIClient) -> List[str]:
    names = []
    for pokemon_name in get_type_pokemon(client, "electric"):
        species_data = client.species(pokemon_name)
        chain_url = species_data.get("evolution_chain", {}).get("url")
        chain_data = client.get_json(chain_url)
        chain = chain_data["chain"]
        stack = [chain]
        has_evolution = False
        while stack:
            node = stack.pop()
            if node["species"]["name"] == species_data["name"] and node.get("evolves_to"):
                has_evolution = True
                break
            stack.extend(node.get("evolves_to", []))
        if not has_evolution and species_data.get("evolves_from_species") is None:
            names.append(species_data["name"])
    return sorted(set(names))


def highest_attack_in_johto(client: PokeAPIClient) -> Tuple[str, int]:
    best: Tuple[str, int] = ("", -1)
    for species in client.paginated_results("pokemon-species?limit=2000"):
        species_data = client.species(species["name"])
        if species_data.get("generation", {}).get("name") != "generation-ii":
            continue
        pokemon_data = get_default_pokemon_for_species(client, species_data)
        if not pokemon_data:
            continue
        for stat in pokemon_data.get("stats", []):
            if stat["stat"]["name"] == "attack":
                if stat["base_stat"] > best[1]:
                    best = (pokemon_data["name"], stat["base_stat"])
                break
    return best


def fastest_non_legendary(client: PokeAPIClient) -> Tuple[str, int]:
    best: Tuple[str, int] = ("", -1)
    for species in client.paginated_results("pokemon-species?limit=2000"):
        species_data = client.species(species["name"])
        if species_data.get("is_legendary"):
            continue
        pokemon_data = get_default_pokemon_for_species(client, species_data)
        if not pokemon_data:
            continue
        for stat in pokemon_data.get("stats", []):
            if stat["stat"]["name"] == "speed":
                if stat["base_stat"] > best[1]:
                    best = (pokemon_data["name"], stat["base_stat"])
                break
    return best


def common_habitat_for_grass(client: PokeAPIClient) -> Tuple[str, int]:
    counter: Dict[str, int] = collections.Counter()
    for pokemon_name in get_type_pokemon(client, "grass"):
        species_data = client.species(pokemon_name)
        habitat = species_data.get("habitat", {}) or {}
        habitat_name = habitat.get("name")
        if habitat_name:
            counter[habitat_name] += 1
    if not counter:
        return ("desconocido", 0)
    habitat_name, count = counter.most_common(1)[0]
    return habitat_name, count


def lightest_pokemon(client: PokeAPIClient) -> Tuple[str, int]:
    best: Tuple[str, int] = ("", 10**9)
    for pokemon in client.paginated_results("pokemon?limit=2000"):
        pokemon_data = client.pokemon(pokemon["name"])
        weight = pokemon_data.get("weight", best[1])
        if weight < best[1]:
            best = (pokemon_data["name"], weight)
    return best


def main() -> None:
    client = PokeAPIClient()

    fire_kanto = fire_pokemon_in_kanto(client)
    tall_water = tall_water_pokemon(client)
    bulbasaur_chain = evolution_chain_for_starter(client, "bulbasaur")
    electric_loners = electric_without_evolutions(client)
    johto_attack = highest_attack_in_johto(client)
    fastest = fastest_non_legendary(client)
    common_habitat, habitat_count = common_habitat_for_grass(client)
    lightest = lightest_pokemon(client)

    print("Pokémon de tipo fuego en Kanto:", fire_kanto)
    print("Pokémon tipo agua con altura >= 11:", tall_water)
    print("Cadena evolutiva de Bulbasaur:", " -> ".join(bulbasaur_chain))
    print("Pokémon eléctricos sin evoluciones:", electric_loners)
    print("Mayor ataque base en Johto:", f"{johto_attack[0]} ({johto_attack[1]})")
    print("Velocidad más alta no legendaria:", f"{fastest[0]} ({fastest[1]})")
    print(
        "Hábitat más común entre los tipo planta:",
        f"{common_habitat} (\"{habitat_count}\" especies)",
    )
    print("Pokémon con menor peso registrado:", f"{lightest[0]} ({lightest[1]} hm)")


if __name__ == "__main__":
    main()
