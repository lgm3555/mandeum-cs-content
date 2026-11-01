---
date: 2026-10-18
slug: java-equals-and-hashcode
title: 자바의 equals와 hashCode
---

## 질문
자바에서 `==`와 `equals()`는 무엇이 다르고, `equals()`를 재정의할 때 `hashCode()`도 함께 재정의해야 하는 이유는 무엇인가요?

## 정답
`==`는 기본형이면 값을, 참조형이면 두 변수가 같은 객체를 가리키는지를 비교합니다. `equals()`는 객체가 논리적으로 같은지를 비교하도록 재정의할 수 있습니다. `HashMap`·`HashSet`은 `hashCode()`로 버킷을 먼저 찾은 뒤 `equals()`로 비교하므로, `equals()`가 같다고 판단한 두 객체는 반드시 같은 `hashCode()`를 반환해야 합니다.

## 해설
### 먼저 한 줄씩 정리해 볼게요

- `==`는 **"같은 물건인가?"**를 묻습니다.
- `equals()`는 **"내용이 같은가?"**를 묻습니다.
- `hashCode()`는 **"몇 번 사물함에 넣을까?"**를 정하는 번호입니다.

### ==와 equals(): 같은 물건 vs 같은 내용

서점에서 같은 책을 두 권 샀다고 생각해 보세요. 제목도 내용도 똑같지만, 책은 분명히 두 권입니다.

- `==`로 비교하면 **다른 책**입니다. 서로 다른 객체이기 때문입니다.
- `equals()`로 비교하면 **같은 책**입니다. 내용이 같기 때문입니다.

```java
String a = new String("java");
String b = new String("java");

a == b;      // false: 책이 두 권 (다른 객체)
a.equals(b); // true: 내용이 같음
```

`String`은 자바가 이미 `equals()`를 "내용 비교"로 만들어 두었습니다. 하지만 **직접 만든 클래스는 그렇지 않습니다.** 재정의하지 않으면 `equals()`도 `==`처럼 "같은 물건인가?"만 확인합니다.

### hashCode()는 왜 같이 바꿔야 할까?

`HashSet`은 물건을 찾을 때 두 단계를 거칩니다.

1. `hashCode()`로 **사물함 번호**를 정합니다.
2. 그 사물함 **안에서만** `equals()`로 비교합니다.

문제는 1단계에서 생깁니다. `equals()`만 바꾸고 `hashCode()`를 그대로 두면, 내용이 같은 두 객체도 서로 다른 사물함 번호를 받습니다. 기본 `hashCode()`는 객체마다 다른 번호를 주기 때문입니다. 결국 `HashSet`은 엉뚱한 사물함만 열어 보고 "없어요"라고 답합니다. `equals()`로 비교할 기회조차 오지 않습니다.

![같은 회원 번호 카드가 왼쪽에서는 서로 다른 사물함 번호를 받아 찾지 못하고, 오른쪽에서는 같은 사물함에서 번호를 대조해 찾는 비교 그림](../images/java-equals-and-hashcode.png)

사물함은 버킷, 사물함 번호는 hashCode, 카드 대조는 equals에 대응하는 비유입니다. HashSet은 고른 사물함 안에서만 비교하므로, 사물함 번호가 다르면 값이 같은 회원도 찾지 못합니다.

### 코드로 확인하기

회원 번호(`id`)가 같으면 같은 회원으로 보도록 `equals()`만 재정의해 보겠습니다.

```java
class Member {
    private final long id;
    Member(long id) { this.id = id; }

    @Override
    public boolean equals(Object o) {
        return o instanceof Member m && id == m.id;
    }
    // hashCode()는 재정의하지 않음
}

Set<Member> members = new HashSet<>();
members.add(new Member(1));
members.contains(new Member(1)); // 대부분 false
```

분명 같은 1번 회원을 넣었는데 찾지 못합니다. 해결 방법은 간단합니다. `equals()`에서 비교한 값으로 `hashCode()`도 **함께 만들어 주면 됩니다.**

```java
@Override
public int hashCode() {
    return Long.hashCode(id); // equals와 같은 기준(id)으로 계산
}
```

이제 같은 `id`는 항상 같은 사물함으로 가므로 `contains()`가 `true`를 반환합니다. 자바 16 이상이라면 `record Member(long id) {}`처럼 `record`를 쓰는 방법도 있습니다. `equals()`와 `hashCode()`를 짝을 맞춰 자동으로 만들어 줍니다.

### 기억할 점

- `equals()`가 같으면 `hashCode()`도 **반드시** 같아야 합니다.
- 반대로 `hashCode()`가 같다고 `equals()`도 같은 것은 아닙니다. 다른 물건이 같은 사물함에 들어갈 수도 있습니다(해시 충돌).
- 사물함에 넣은 뒤 `id`를 바꾸면 사물함 번호도 바뀌어 다시 찾지 못합니다. 키로 쓰는 객체는 값이 바뀌지 않게(불변) 만드는 것이 안전합니다.

### 참고 자료

- [Oracle Java — Object (equals, hashCode)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html)
