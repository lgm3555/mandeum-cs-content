---
date: 2026-11-27
slug: database-composite-index-order
title: 복합 인덱스의 컬럼 순서
---

## 질문
(last_name, first_name) 순서로 복합 인덱스를 만들었습니다. WHERE first_name = '민수'만으로 조회하면 이 인덱스를 효율적으로 사용할 수 있나요? 복합 인덱스의 컬럼 순서는 어떻게 정해야 하나요?

## 정답
대부분의 경우 효율적으로 사용하기 어렵습니다. 복합 인덱스는 첫 번째 컬럼으로 정렬하고, 그 값이 같을 때만 두 번째 컬럼으로 정렬합니다. 그래서 첫 컬럼인 `last_name` 조건 없이 `first_name`만으로는 찾을 범위를 좁힐 수 없습니다.

컬럼 순서는 자주 쓰는 조회 조건을 기준으로 정합니다. 보통 항상 함께 쓰이는 등호(`=`) 조건 컬럼을 앞에, 범위 조건(`>`, `BETWEEN`)이나 정렬에 쓰이는 컬럼을 뒤에 둡니다.

## 해설
### 전화번호부를 떠올려 보세요

전화번호부가 성, 이름 순으로 정렬되어 있다면 "김민수"는 빨리 찾을 수 있습니다. 성이 "김"인 구간으로 이동한 뒤 그 안에서 "민수"를 찾으면 되기 때문입니다.

하지만 성을 모른 채 이름이 "민수"인 사람을 모두 찾으려면 처음부터 끝까지 넘겨 봐야 합니다. "민수"는 김, 이, 박 구간에 흩어져 있기 때문입니다.

![성 순서로 칸이 나뉜 책장에서 "김" 칸으로 바로 가 "민수"를 찾는 왼쪽 장면과, 성을 모른 채 모든 칸을 하나씩 뒤지는 오른쪽 장면의 비교 그림](../images/database-composite-index-order.png)

책장의 칸은 첫 번째 컬럼, 칸 안의 순서는 두 번째 컬럼에 대응하는 비유입니다. 첫 번째 컬럼을 알아야 바로 해당 칸으로 이동할 수 있습니다.

### 사용할 수 있는 조건과 어려운 조건

```sql
CREATE INDEX idx_name ON members (last_name, first_name);

-- 인덱스로 범위를 좁힐 수 있음
SELECT * FROM members WHERE last_name = '김';
SELECT * FROM members WHERE last_name = '김' AND first_name = '민수';

-- 인덱스로 범위를 좁히기 어려움
SELECT * FROM members WHERE first_name = '민수';
```

앞쪽 컬럼부터 차례로 조건이 있어야 인덱스를 따라 찾아갈 수 있습니다. 이를 왼쪽 접두사(leftmost prefix) 규칙이라고 부릅니다. 일부 DB는 첫 컬럼의 값 종류가 적을 때 건너뛰며 찾는 기능을 제공하지만, 항상 기대할 수 있는 동작은 아닙니다.

### 등호는 앞에, 범위는 뒤에

```sql
-- 자주 쓰는 조회
SELECT * FROM orders
WHERE customer_id = 42 AND created_at >= '2026-11-01';
```

이 조회에는 `(customer_id, created_at)` 인덱스가 잘 맞습니다. 고객 42번의 구간으로 이동한 뒤, 그 안에서 날짜 순으로 정렬된 범위만 읽으면 됩니다.

반대로 `(created_at, customer_id)`로 만들면 11월 이후의 모든 주문을 날짜 순으로 훑으면서 고객 번호를 하나씩 확인해야 합니다. 범위 조건 뒤에 오는 컬럼은 탐색 범위를 좁히는 데 쓰이기 어렵습니다.

### 기억할 점

- 인덱스는 실제로 자주 실행되는 쿼리의 조건과 정렬을 보고 설계합니다.
- 인덱스를 추가하면 쓰기 작업마다 인덱스도 함께 갱신해야 하므로, 많이 만든다고 좋은 것은 아닙니다.
- 실행 계획(`EXPLAIN`)으로 인덱스가 실제로 사용되는지 확인합니다.

### 참고 자료

- [PostgreSQL — Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [MySQL — Multiple-Column Indexes](https://dev.mysql.com/doc/refman/8.4/en/multiple-column-indexes.html)
