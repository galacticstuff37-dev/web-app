// Единый справочник растений. Извлечён из PLANTS в proto.py скриптом,
// значения не редактировались. kind: house — декоративные, edible — съедобные.
// cool=true у съедобных — холодостойкая культура: сеется до последних
// заморозков и терпит их. img=null означает «настоящей фотографии нет».

export type Kind = "house" | "edible";

export interface Species {
  id: string; name: string; kind: Kind; icon: string; latin: string;
  water: number; light: string; hum: string; img: string | null;
  days: number; daysMax: number; pot: string; sun: number;
  tags: string[]; sill: boolean; cool: boolean;
}

export const SPECIES: Species[] = [
  {
    "id": "monstera",
    "name": "Monstera",
    "kind": "house",
    "icon": "leaf",
    "latin": "Monstera deliciosa",
    "water": 9,
    "light": "Bright indirect",
    "hum": "Medium",
    "img": "monstera",
    "days": 0,
    "daysMax": 0,
    "pot": "10 inch",
    "sun": 1,
    "tags": [
      "statement",
      "trailing"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "snakeplant",
    "name": "Snake plant",
    "kind": "house",
    "icon": "plant",
    "latin": "Dracaena trifasciata",
    "water": 18,
    "light": "Low to bright",
    "hum": "Low",
    "img": "snakeplant",
    "days": 0,
    "daysMax": 0,
    "pot": "8 inch",
    "sun": 1,
    "tags": [
      "hardy",
      "lowlight",
      "air"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "pothos",
    "name": "Pothos",
    "kind": "house",
    "icon": "leaf",
    "latin": "Epipremnum aureum",
    "water": 8,
    "light": "Low to bright",
    "hum": "Medium",
    "img": "pothos",
    "days": 0,
    "daysMax": 0,
    "pot": "6 inch",
    "sun": 1,
    "tags": [
      "hardy",
      "lowlight",
      "trailing",
      "air",
      "kids"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "zzplant",
    "name": "ZZ plant",
    "kind": "house",
    "icon": "plant",
    "latin": "Zamioculcas zamiifolia",
    "water": 18,
    "light": "Low light",
    "hum": "Low",
    "img": "zzplant",
    "days": 0,
    "daysMax": 0,
    "pot": "8 inch",
    "sun": 1,
    "tags": [
      "hardy",
      "lowlight"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "fiddleleaf",
    "name": "Fiddle leaf fig",
    "kind": "house",
    "icon": "leaf",
    "latin": "Ficus lyrata",
    "water": 9,
    "light": "Bright indirect",
    "hum": "Medium",
    "img": "fiddleleaf",
    "days": 0,
    "daysMax": 0,
    "pot": "12 inch",
    "sun": 2,
    "tags": [
      "statement"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "peacelily",
    "name": "Peace lily",
    "kind": "house",
    "icon": "flower",
    "latin": "Spathiphyllum wallisii",
    "water": 6,
    "light": "Medium indirect",
    "hum": "High",
    "img": "peacelily",
    "days": 0,
    "daysMax": 0,
    "pot": "8 inch",
    "sun": 1,
    "tags": [
      "flowers",
      "air"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "aloe",
    "name": "Aloe vera",
    "kind": "house",
    "icon": "plant",
    "latin": "Aloe vera",
    "water": 18,
    "light": "Bright direct",
    "hum": "Low",
    "img": "aloe",
    "days": 0,
    "daysMax": 0,
    "pot": "6 inch",
    "sun": 3,
    "tags": [
      "hardy",
      "useful"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "calathea",
    "name": "Calathea",
    "kind": "house",
    "icon": "leaf",
    "latin": "Goeppertia orbifolia",
    "water": 6,
    "light": "Medium indirect",
    "hum": "High",
    "img": "calathea",
    "days": 0,
    "daysMax": 0,
    "pot": "8 inch",
    "sun": 1,
    "tags": [
      "statement",
      "petsafe"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "radish",
    "name": "Radish",
    "kind": "edible",
    "icon": "carrot",
    "latin": "Raphanus sativus",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "radish",
    "days": 25,
    "daysMax": 35,
    "pot": "1 pint",
    "sun": 1,
    "tags": [
      "fast",
      "roots",
      "kids"
    ],
    "sill": false,
    "cool": true
  },
  {
    "id": "lettuce",
    "name": "Leaf lettuce",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Lactuca sativa",
    "water": 2,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "lettuce",
    "days": 30,
    "daysMax": 35,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "salads",
      "fast"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "chard",
    "name": "Swiss chard",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Beta vulgaris",
    "water": 2,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "chard",
    "days": 30,
    "daysMax": 40,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "salads"
    ],
    "sill": false,
    "cool": true
  },
  {
    "id": "mustard",
    "name": "Mustard greens",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Brassica juncea",
    "water": 2,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "mustard",
    "days": 35,
    "daysMax": 40,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "salads"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "microgreens",
    "name": "Microgreens",
    "kind": "edible",
    "icon": "grains",
    "latin": "",
    "water": 1,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "microgreens",
    "days": 10,
    "daysMax": 14,
    "pot": "tray",
    "sun": 1,
    "tags": [
      "fast",
      "herbs",
      "kids"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "cilantro",
    "name": "Cilantro",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Coriandrum sativum",
    "water": 3,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "cilantro",
    "days": 28,
    "daysMax": 42,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "herbs",
      "fast"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "basil",
    "name": "Basil",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Ocimum basilicum",
    "water": 3,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "basil",
    "days": 40,
    "daysMax": 40,
    "pot": "1 gal",
    "sun": 2,
    "tags": [
      "herbs"
    ],
    "sill": true,
    "cool": false
  },
  {
    "id": "beans",
    "name": "Bush beans",
    "kind": "edible",
    "icon": "grains",
    "latin": "Phaseolus vulgaris",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "beans",
    "days": 45,
    "daysMax": 60,
    "pot": "2 gal",
    "sun": 2,
    "tags": [
      "beans",
      "kids"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "beets",
    "name": "Beets",
    "kind": "edible",
    "icon": "carrot",
    "latin": "Beta vulgaris",
    "water": 2,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "beets",
    "days": 50,
    "daysMax": 60,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "roots"
    ],
    "sill": false,
    "cool": true
  },
  {
    "id": "squash",
    "name": "Summer squash",
    "kind": "edible",
    "icon": "orange",
    "latin": "Cucurbita pepo",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "squash",
    "days": 50,
    "daysMax": 60,
    "pot": "5 gal",
    "sun": 2,
    "tags": [],
    "sill": false,
    "cool": false
  },
  {
    "id": "cherrytomato",
    "name": "Cherry tomato",
    "kind": "edible",
    "icon": "cherries",
    "latin": "Solanum lycopersicum",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "cherrytomato",
    "days": 55,
    "daysMax": 100,
    "pot": "1 gal",
    "sun": 2,
    "tags": [
      "tomatoes",
      "kids"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "tomato",
    "name": "Tomato",
    "kind": "edible",
    "icon": "cherries",
    "latin": "Solanum lycopersicum",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "tomato",
    "days": 55,
    "daysMax": 100,
    "pot": "5 gal",
    "sun": 2,
    "tags": [
      "tomatoes"
    ],
    "sill": false,
    "cool": false
  },
  {
    "id": "kale",
    "name": "Kale",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Brassica oleracea",
    "water": 2,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "kale",
    "days": 55,
    "daysMax": 65,
    "pot": "5 gal",
    "sun": 1,
    "tags": [
      "salads"
    ],
    "sill": false,
    "cool": true
  },
  {
    "id": "turnips",
    "name": "Turnips",
    "kind": "edible",
    "icon": "carrot",
    "latin": "Brassica rapa",
    "water": 2,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "turnips",
    "days": 30,
    "daysMax": 60,
    "pot": "3 gal",
    "sun": 1,
    "tags": [
      "roots"
    ],
    "sill": false,
    "cool": true
  },
  {
    "id": "carrots",
    "name": "Carrots",
    "kind": "edible",
    "icon": "carrot",
    "latin": "Daucus carota",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "carrots",
    "days": 65,
    "daysMax": 80,
    "pot": "1 quart",
    "sun": 1,
    "tags": [
      "roots",
      "kids"
    ],
    "sill": false,
    "cool": true
  },
  {
    "id": "cucumber",
    "name": "Cucumber",
    "kind": "edible",
    "icon": "orange",
    "latin": "Cucumis sativus",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "cucumber",
    "days": 70,
    "daysMax": 80,
    "pot": "5 gal",
    "sun": 2,
    "tags": [],
    "sill": false,
    "cool": false
  },
  {
    "id": "onions",
    "name": "Green onions",
    "kind": "edible",
    "icon": "plant",
    "latin": "Allium fistulosum",
    "water": 3,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "onions",
    "days": 70,
    "daysMax": 100,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "herbs"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "parsley",
    "name": "Parsley",
    "kind": "edible",
    "icon": "leaf",
    "latin": "Petroselinum crispum",
    "water": 3,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "parsley",
    "days": 70,
    "daysMax": 84,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "herbs"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "eggplant",
    "name": "Eggplant",
    "kind": "edible",
    "icon": "pepper",
    "latin": "Solanum melongena",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "eggplant",
    "days": 75,
    "daysMax": 100,
    "pot": "5 gal",
    "sun": 2,
    "tags": [],
    "sill": false,
    "cool": false
  },
  {
    "id": "chives",
    "name": "Garlic chives",
    "kind": "edible",
    "icon": "plant",
    "latin": "Allium tuberosum",
    "water": 3,
    "light": "3–5 h sun",
    "hum": "—",
    "img": "chives",
    "days": 84,
    "daysMax": 84,
    "pot": "0.5 gal",
    "sun": 1,
    "tags": [
      "herbs"
    ],
    "sill": true,
    "cool": true
  },
  {
    "id": "pepper",
    "name": "Bell pepper",
    "kind": "edible",
    "icon": "pepper",
    "latin": "Capsicum annuum",
    "water": 2,
    "light": "6–8 h sun",
    "hum": "—",
    "img": "pepper",
    "days": 110,
    "daysMax": 120,
    "pot": "2 gal",
    "sun": 2,
    "tags": [
      "peppers"
    ],
    "sill": false,
    "cool": false
  }
];

export const SP = (id: string) => SPECIES.find(s => s.id === id);
export const ofKind = (k: Kind) => SPECIES.filter(s => s.kind === k);
export const N_HOUSE = SPECIES.filter(s => s.kind === "house").length;
export const N_EDIBLE = SPECIES.filter(s => s.kind === "edible").length;
