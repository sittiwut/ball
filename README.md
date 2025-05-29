<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>สูตรฟีโบนักชีแบบปรับกลับ</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f5f7fa;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      background: #fff;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      width: 320px;
      text-align: center;
    }
    h1 {
      margin-bottom: 1rem;
      font-size: 1.4rem;
      color: #333;
    }
    button {
      padding: 10px 20px;
      margin: 0 10px;
      font-size: 1rem;
      border-radius: 8px;
      border: none;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    button.win {
      background-color: #4CAF50;
      color: white;
    }
    button.win:hover {
      background-color: #45a049;
    }
    button.lose {
      background-color: #f44336;
      color: white;
    }
    button.lose:hover {
      background-color: #da190b;
    }
    p {
      font-size: 1.2rem;
      margin: 1rem 0 0.5rem;
      color: #555;
    }
    #log {
      margin-top: 1rem;
      max-height: 180px;
      overflow-y: auto;
      text-align: left;
      font-size: 0.9rem;
      background: #f0f4f8;
      padding: 10px;
      border-radius: 8px;
      box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
    }
    #log div {
      margin-bottom: 6px;
    }
    #resetBtn {
      margin-top: 15px;
      background-color: #007bff;
      color: white;
      padding: 8px 16px;
      border-radius: 8px;
      border: none;
      cursor: pointer;
      font-size: 1rem;
    }
    #resetBtn:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>สูตรฟีโบนักชีแบบปรับกลับ</h1>
    <p>ไม้ที่: <strong id="step">1</strong> / 10</p>
    <p>จำนวนเดิมพัน: <strong id="bet">1</strong> หน่วย</p>
    <div>
      <button class="lose" onclick="handleLose()">แพ้</button>
      <button class="win" onclick="handleWin()">ชนะ</button>
    </div>
    <button id="resetBtn" onclick="resetGame()">รีเซ็ต</button>
    <div id="log"></div>
  </div>

  <script>
    const fibSequence = [1,1,2,3,5,8,13,21,34,55];
    let currentStep = 0;  // index เริ่มที่ 0 คือไม้ที่ 1
    let winStreak = 0;
    const maxStep = 9;    // ไม้ที่ 10 คือ index 9
    const stepElem = document.getElementById('step');
    const betElem = document.getElementById('bet');
    const logDiv = document.getElementById('log');

    function log(message) {
      const entry = document.createElement('div');
      entry.textContent = message;
      logDiv.prepend(entry);
    }

    function updateDisplay() {
      stepElem.textContent = currentStep + 1;
      betElem.textContent = fibSequence[currentStep];
    }

    function handleLose() {
      winStreak = 0;
      if (currentStep < maxStep) {
        currentStep++;
        log(`❌ แพ้ → เดินหน้าไม้ที่ ${currentStep + 1} เดิมพัน ${fibSequence[currentStep]} หน่วย`);
      } else {
        log('⚠️ ถึงไม้ที่ 10 แล้วยังไม่ชนะติด 2 ไม้ → หยุดเล่น');
        alert('หยุดเล่น: ถึงไม้ที่ 10 แล้วยังไม่ชนะติด 2 ไม้');
      }
      updateDisplay();
    }

    function handleWin() {
      winStreak++;
      currentStep -= 2;
      if (currentStep < 0) currentStep = 0;

      log(`✅ ชนะ → ถอยหลัง 2 ขั้น เหลือไม้ที่ ${currentStep + 1} เดิมพัน ${fibSequence[currentStep]} หน่วย`);

      if (winStreak >= 2) {
        log('🎉 ชนะติดกัน 2 ไม้ → รีเซ็ตสูตร');
        resetGame();
      }
      updateDisplay();
    }

    function resetGame() {
      currentStep = 0;
      winStreak = 0;
      updateDisplay();
      log('🔄 รีเซ็ตสูตร กลับสู่ไม้ที่ 1');
    }

    updateDisplay();
  </script>
</body>
</html>
