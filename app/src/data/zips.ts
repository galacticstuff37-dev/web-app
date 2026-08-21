// ZIP-ы с данными по заморозкам. Извлечены из ZIPS в proto.py.
// frost — средняя дата последних весенних заморозков, season — длина
// сезона в днях до первых осенних.

export interface Zip { zip: string; city: string; zone: string; frost: string; season: number }

export const ZIPS: Zip[] = [
  { zip: "78704", city: "Austin, TX", zone: "8b", frost: "Mar 3", season: 270 },
  { zip: "97214", city: "Portland, OR", zone: "8b", frost: "Apr 5", season: 230 },
  { zip: "10025", city: "New York, NY", zone: "7b", frost: "Apr 15", season: 200 },
  { zip: "60613", city: "Chicago, IL", zone: "6a", frost: "May 5", season: 170 },
];
