// 상단에 npm으로 설치한 패키지 express를 불러옴.
// const로 선언하여 다른 값으로 덮어쓰는 것 방지.

const express = require("express");

// express 인스턴스 생성
const app = express();

// 라우트 추가
// 인터넷의 주소에 대응, "/"의 경우에는 root 페이지를 뜻한다.
app.get("/", (req, res) => {
    res.send("Hello World~!");
});

// Json을 출력해주는 라우트
app.get("/posts", function (req, res){
    res.json([
        {postId: 1, title: "Hello!"},
        {postId: 2, title: "World!"}
    ]);
});

// 어떤 포트를 통해 서버에 접속하게 할 것인지 지정
// process.env.PORT: 서버의 환경 변수에 등록된 PORT 정보를 이용
// 만약에 환경 변수에 PORT 정보가 등록되어 있지 않다면 8000번을 기본 값으로 이용
const PORT = process.env.PORT || 8000;

// 서버가 PORT에 연결되었을 때 수행할 함수 정의
app.listen(PORT, () => {
   console.log("서버가 실행됐습니다.");
   console.log(`서버주소: http://localhost:${PORT}`);
});