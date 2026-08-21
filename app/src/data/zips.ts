// ZIP-ы с датами заморозков.
//
// Раньше здесь лежала одна дата плюс длина сезона числом, и вторая дата
// выводилась сложением. Числа не сходились со станционными нормалями: у трёх
// городов из четырёх сезон расходился на 28–33 дня, а от этих дат считается
// весь календарь. Теперь хранятся ОБЕ даты, сезон считается из них.
//
// Austin / Portland / Chicago сверены с публикуемыми станционными датами
// (AUSTIN 6S, PORTLAND KGW-TV, CHICAGO NORTHERLY IS; источник — нормали NOAA
// 1991–2020). Нью-Йорк остаётся как был: его станцию не сверяли, а выдумывать
// дату нельзя — она поедет по всем окнам сразу.

export interface Zip {
  zip: string
  city: string
  zone: string
  /** последние весенние заморозки */
  last: string
  /** первые осенние */
  first: string
  /** true — даты сверены со станцией; false — унаследованы и требуют сверки */
  checked: boolean
}

export const ZIPS: Zip[] = [
  { zip: '78704', city: 'Austin, TX',   zone: '8b', last: 'Mar 18', first: 'Nov 10', checked: true },
  { zip: '97214', city: 'Portland, OR', zone: '8b', last: 'Mar 6',  first: 'Nov 22', checked: true },
  { zip: '10025', city: 'New York, NY', zone: '7b', last: 'Apr 15', first: 'Nov 1',  checked: false },
  { zip: '60613', city: 'Chicago, IL',  zone: '6a', last: 'Apr 17', first: 'Nov 1',  checked: true },
]
