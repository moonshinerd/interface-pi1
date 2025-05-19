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
      resultDiv.style.backgroundColor = '#0fa143';
      resultDiv.style.color = 'white';
      resultDiv.innerHTML = `<strong>Distância selecionada:</strong> ${dist} m`;

      resultDiv.classList.add('active');

      btn.textContent = 'Iniciar Cálculo';
      btn.disabled = false;
    }, 500);
  });
});
