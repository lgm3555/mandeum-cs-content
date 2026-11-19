---
date: 2026-11-24
slug: java-garbage-collection
title: Java 가비지 컬렉션의 기준
---

## 질문
Java의 가비지 컬렉터(GC)는 어떤 객체를 "더 이상 쓰지 않는다"고 판단해 메모리에서 정리하나요? GC가 있는데도 메모리 누수가 생길 수 있는 이유는 무엇인가요?

## 정답
GC는 스택의 지역 변수, static 필드 같은 GC 루트에서 참조를 따라가 도달할 수 있는 객체를 "살아 있다"고 봅니다. 어떤 경로로도 도달할 수 없는 객체는 프로그램이 다시 사용할 방법이 없으므로 정리 대상이 됩니다.

GC는 "도달할 수 있는 객체"를 지우지 않습니다. 더 이상 필요 없는 객체라도 static 컬렉션이나 캐시에 참조가 계속 남아 있으면 정리되지 않습니다. 이렇게 쓰지 않는 객체를 계속 붙잡고 있는 것이 Java에서의 메모리 누수입니다.

## 해설
### 기준은 "도달할 수 있는가"

```java
void process() {
    User user = new User("kim"); // user 변수가 객체를 참조
    user = null;                 // 이제 이 객체로 가는 길이 없음
}
```

`user = null` 이후에는 `User` 객체로 가는 참조가 없습니다. 이 객체는 GC가 정리할 수 있는 상태가 됩니다. 메서드가 끝나 지역 변수가 사라질 때도 마찬가지입니다.

![중앙 기둥에서 출발한 밧줄이 연결된 풍선들은 떠 있고, 밧줄이 끊어진 풍선들은 청소 로봇이 거두어 가는 그림](../images/java-garbage-collection.png)

기둥은 GC 루트, 밧줄은 참조, 풍선은 객체에 대응하는 비유입니다. 기둥에서 밧줄을 따라 이어진 풍선만 남고, 연결이 끊어진 풍선은 정리됩니다.

### 서로만 가리키는 객체도 정리돼요

객체 A가 B를, B가 A를 가리키더라도 GC 루트에서 두 객체로 가는 길이 없으면 둘 다 정리 대상입니다. Java의 GC는 참조 개수를 세는 방식이 아니라 루트에서 도달 가능한지를 따지기 때문입니다.

### 세대별로 나누어 관리하기

대부분의 객체는 만들어진 뒤 금방 쓰이지 않게 됩니다. 그래서 JVM은 힙을 새 객체가 모이는 Young 영역과 오래 살아남은 객체가 옮겨지는 Old 영역으로 나누어 관리합니다. Young 영역은 자주, 빠르게 정리하고 Old 영역은 상대적으로 드물게 정리합니다.

GC가 동작하는 동안 애플리케이션 스레드가 잠시 멈추는 구간이 생길 수 있습니다. 최근 JVM의 기본 GC인 G1이나 ZGC 같은 수집기는 이 멈춤 시간을 줄이도록 설계되었습니다.

### GC가 있어도 생기는 메모리 누수

```java
class SessionStore {
    private static final Map<String, Session> SESSIONS = new HashMap<>();

    static void login(String id, Session session) {
        SESSIONS.put(id, session);
    }
    // 로그아웃해도 remove하지 않는다면?
}
```

static 필드는 GC 루트에서 계속 도달할 수 있습니다. 로그아웃한 세션을 지우지 않으면 맵이 계속 커지고, 결국 `OutOfMemoryError`가 발생할 수 있습니다.

### 기억할 점

- 더 이상 필요 없는 객체는 컬렉션에서 제거하거나, 캐시에는 최대 크기와 만료 정책을 둡니다.
- `System.gc()`는 GC를 요청하는 힌트일 뿐 즉시 실행을 보장하지 않습니다.
- 파일이나 DB 연결 같은 자원은 GC에 맡기지 말고 `try-with-resources`로 직접 닫습니다.

### 참고 자료

- [Oracle — HotSpot Virtual Machine Garbage Collection Tuning Guide](https://docs.oracle.com/en/java/javase/21/gctuning/introduction-garbage-collection-tuning.html)
