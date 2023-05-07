import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import "./App.css";

function Navbar() {
  return (
    <div className="navbar">
      <a href="/">
        <h3>ATM LOGO</h3>
      </a>
      <ul>
        <li>
          <a href="/menu1">ATM이란?</a>
        </li>
        <li>
          <a href="/menu2">ATM 사용하기</a>
        </li>
        <li>
          <a href="/menu3">백테스트</a>
        </li>
        <li>
          <a href="/menu4">ATM 메뉴얼</a>
        </li>
      </ul>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
      {/* navbar 외의 주요 컨텐츠를 여기에 추가 */}
    </div>
  );
}

export default App;
