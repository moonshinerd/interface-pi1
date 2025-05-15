document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('calc-btn');
  const resultDiv = document.getElementById('result');
  const select = document.getElementById('distance');

  btn.addEventListener('click', () => {
    // Feedback inicial
    btn.textContent = 'Calculando…';
    btn.disabled = true;

    // Simula o cálculo
    setTimeout(() => {
      const dist = select.value;
      resultDiv.innerHTML = `<span style="color:rgb(134, 15, 106);"><strong>Distância selecionada:</strong> ${dist} m</span>`;
      resultDiv.classList.add('active');

      // Restaura o botão
      btn.textContent = 'Iniciar Cálculo';
      btn.disabled = false;
    }, 500);
  });
});
