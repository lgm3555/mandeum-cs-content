---
date: 2026-10-18
slug: java-equals-and-hashcode
title: 자바의 equals와 hashCode
---

## 질문
Java에서 == 연산자와 equals() 메서드는 객체를 비교하는 방식에서 어떤 차이가 있나요? 또한, equals()를 재정의할 때 hashCode()도 함께 재정의해야 하는 이유는 무엇인가요?

## 정답
==는 기본형에서는 값이 같은지, 참조형에서는 같은 객체를 가리키는지 비교합니다.

equals()는 정해진 기준에 따라 두 객체를 같다고 볼 수 있는지 비교합니다. 예를 들어 문자열은 내용이 같으면, 회원은 회원 번호가 같으면 같은 것으로 판단할 수 있습니다.

HashMap과 HashSet은 hashCode()로 검색할 위치를 좁힌 뒤 equals()로 같은 객체인지 확인합니다. 따라서 equals()가 true인 두 객체는 반드시 같은 hashCode()를 반환해야 합니다. 이 규칙을 지키도록 두 메서드를 함께 재정의해야 합니다.

## 해설
### `==`와 `equals()`는 무엇을 비교할까요?

같은 책을 두 권 샀다고 생각해 보세요. 내용은 같지만, 손에 들고 있는 책은 서로 다른 두 권입니다.

객체를 비교할 때도 이 차이가 있습니다.

* `==`: 둘이 실제로 같은 객체인가?
* `equals()`: 둘을 같은 것으로 볼 수 있는가?

문자열로 확인하면 더 쉽습니다.

```java
String a = new String("java");
String b = new String("java");

System.out.println(a == b);      // false: 서로 다른 객체
System.out.println(a.equals(b)); // true: 문자열 내용이 같음
```

`new`로 각각 만들었기 때문에 `a`와 `b`는 서로 다른 객체입니다. 그래서 `==`는 `false`입니다.

하지만 `String`은 문자열의 내용을 비교하도록 `equals()`를 재정의해 두었기 때문에 `a.equals(b)`는 `true`입니다.

직접 만든 클래스도 자동으로 내용을 비교해 주는 것은 아닙니다. `Object`에서 물려받은 기본 `equals()`는 `==`처럼 같은 객체인지 확인합니다. 회원 번호처럼 특정 값을 기준으로 비교하려면 직접 재정의해야 합니다.

### `hashCode()`는 어떤 역할을 할까요?

`HashSet`이 객체를 보관하는 방식을 사물함에 비유해 보겠습니다.

1. `hashCode()`를 바탕으로 객체를 보관할 사물함을 정합니다.
2. 객체를 찾을 때도 같은 방식으로 사물함을 고릅니다.
3. 그 안에서 `equals()`로 같은 객체인지 확인합니다.

여기서 사물함은 버킷, `hashCode()`는 버킷을 고르는 데 사용하는 값입니다. `hashCode()` 자체가 버킷 번호인 것은 아닙니다.

핵심은 처음부터 모든 객체를 하나씩 비교하지 않는다는 것입니다. 해시값으로 찾을 위치를 좁히기 때문에 객체를 빠르게 검색할 수 있습니다.

### `equals()`만 재정의하면 왜 문제가 생길까요?

회원 번호가 같으면 같은 회원으로 판단하도록 `equals()`를 만들었다고 해 보겠습니다.

그런데 `hashCode()`는 그대로 두면, 같은 회원 번호를 가진 두 객체가 서로 다른 해시값을 반환할 수 있습니다.

그러면 같은 회원인데도 서로 다른 사물함으로 안내될 수 있습니다. `HashSet`은 다른 사물함까지 전부 찾아보지 않으므로, 이미 저장한 회원을 찾지 못할 수 있습니다.

![같은 회원 번호 카드가 왼쪽에서는 서로 다른 사물함 번호를 받아 찾지 못하고, 오른쪽에서는 같은 사물함에서 번호를 대조해 찾는 비교 그림](../images/java-equals-and-hashcode.png)

사물함은 버킷, 카드 대조는 equals에 대응하는 비유입니다. 그림에서는 이해를 돕기 위해 해시값으로 고른 사물함 번호를 그대로 표시했습니다. 고른 사물함 안에서만 비교하므로, 사물함이 다르면 값이 같은 회원도 찾지 못합니다.

그래서 다음 규칙이 필요합니다.

`equals()`로 같다고 판단한 두 객체는 반드시 같은 `hashCode()`를 반환해야 합니다.

참고로 기본 `hashCode()`가 객체마다 반드시 다른 값을 반환하는 것은 아닙니다. 다만, 직접 정한 비교 기준에 맞춰 같은 값을 반환한다고 보장하지 않습니다.

### 코드로 확인해 볼까요?

다음은 회원 번호인 `id`가 같으면 같은 회원으로 판단하는 클래스입니다.

```java
final class Member {
    private final long id;

    Member(long id) {
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof Member m && id == m.id;
    }

    // hashCode()는 재정의하지 않음
}
```

두 객체를 직접 비교하면 같은 회원으로 판단합니다.

```java
Member a = new Member(1);
Member b = new Member(1);

System.out.println(a.equals(b)); // true
```

하지만 `HashSet`에서는 문제가 생길 수 있습니다.

```java
Set<Member> members = new HashSet<>();
members.add(a);

System.out.println(members.contains(b)); // false가 나올 수 있음
```

`a`와 `b`는 회원 번호가 같지만, 해시값까지 같다는 보장은 없기 때문입니다.

해결하려면 `equals()`에서 사용한 기준에 맞춰 `hashCode()`도 재정의하면 됩니다.

```java
@Override
public int hashCode() {
    return Long.hashCode(id);
}
```

이제 같은 `id`를 가진 객체는 같은 해시값을 반환합니다. 같은 버킷에서 비교할 수 있고, `equals()`도 `true`이므로 정상적으로 찾습니다.

```java
System.out.println(members.contains(new Member(1))); // true
```

Java 16 이상에서는 다음처럼 `record`를 사용할 수도 있습니다.

```java
record Member(long id) {}
```

`record`는 구성 요소인 `id`를 기준으로 `equals()`와 `hashCode()`를 자동으로 만들어 줍니다.

### 기억할 점

* `equals()`가 `true`이면 `hashCode()`도 반드시 같아야 합니다.
* `hashCode()`가 같아도 `equals()`는 `false`일 수 있습니다. 서로 다른 객체가 같은 해시값을 갖는 것을 해시 충돌이라고 합니다.
* 저장한 뒤 비교 기준이 되는 값을 바꾸면 검색에 문제가 생길 수 있습니다. `HashMap`의 키나 `HashSet`의 원소로 사용할 객체는 해당 값이 바뀌지 않도록 만드는 것이 안전합니다.

### 참고 자료

- [Oracle Java — Object (equals, hashCode)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html)
