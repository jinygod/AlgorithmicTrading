import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import "./App.css";
import Menu1 from "./components/Menu1";
import Menu2 from "./components/Menu2";
import Menu3 from "./components/Menu3";

function Navbar() {
  return (
    <div className="navbar">
      <Link to="/">
        <h3>ATM LOGO</h3>
      </Link>
      <ul>
        <li>
          <Link to="/menu1">ATM이란?</Link>
        </li>
        <li>
          <Link to="/menu2">ATM 사용하기</Link>
        </li>
        <li>
          <Link to="/menu3">백테스트</Link>
        </li>
        <li>
          <Link to="/menu4">ATM 메뉴얼</Link>
        </li>
      </ul>
    </div>
  );
}

function Home() {
  return (
    <div>
      <h2>홈페이지</h2>
      <p>이곳은 홈페이지의 내용입니다.</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/menu1" element={<Menu1 />} />
          <Route path="/menu2" element={<Menu2 />} />
          <Route path="/menu3" element={<Menu3 />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
