import React from "react";
import "./App.css";

function Sidebar() {
  return (
    <div className="sidebar">
      <h3>ATM 이란?</h3>
      <ul>
        <li></li>
        <li>항목 2</li>
        <li>항목 3</li>
      </ul>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <Sidebar />
      {/* 사이드바 외의 주요 컨텐츠를 여기에 추가 */}
    </div>
  );
}

export default App;
