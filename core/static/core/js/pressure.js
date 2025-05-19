document.addEventListener('DOMContentLoaded', () => {
  const fixedVolume = 750;  // mL
  const fixedAngle = 45;    // graus
  const minPressure = 10;   // PSI mínimo seguro
  const maxPressure = 100;  // PSI máximo seguro

  // Modelo simples para calcular pressão recomendada
  function calculateRecommendedPressure(volume, angle) {
    const k = 0.1; // constante do modelo
    return parseFloat((k * volume * Math.sin(angle * (Math.PI / 180))).toFixed(2));
  }

  // Elementos da interface
  const recommendedPressureInput = document.getElementById('recommended-pressure');
  const pressureInput = document.getElementById('pressure');
  const pressureError = document.getElementById('pressure-error');
  const confirmButton = document.getElementById('calc-btn');
  const resultDiv = document.getElementById('result');

  // Calcula e exibe pressão recomendada ao carregar a página
  const recommendedPressure = calculateRecommendedPressure(fixedVolume, fixedAngle);
  recommendedPressureInput.value = `${recommendedPressure} PSI`;
  pressureInput.value = `${recommendedPressure} PSI`;

  // Função para extrair valor numérico da pressão (removendo ' PSI')
  function parsePressure(value) {
    return parseFloat(value.replace(' PSI', '').trim());
  }

  // Validação da pressão ajustada manualmente
  pressureInput.addEventListener('input', () => {
    const val = parsePressure(pressureInput.value);
    if (isNaN(val) || val < minPressure || val > maxPressure) {
      pressureError.textContent = `Pressão fora do intervalo seguro (${minPressure} - ${maxPressure} PSI)`;
      confirmButton.disabled = true;
      resultDiv.innerHTML = ''; // limpa resultado ao errar
    } else {
      pressureError.textContent = '';
      confirmButton.disabled = false;
    }
  });

  // Confirmação da pressão configurada ao clicar no botão
  confirmButton.addEventListener('click', () => {
    const val = parsePressure(pressureInput.value);
    if (pressureError.textContent) {
      alert('Ajuste a pressão para um valor válido antes de confirmar.');
      return;
    }
    // Feedback de sucesso
    resultDiv.style.backgroundColor = '#0fa143';
    resultDiv.style.color = 'white';
    resultDiv.innerHTML = `<strong>Pressão definida com sucesso:</strong> ${val} PSI`;

    alert(`Pressão configurada com sucesso: ${val} PSI`);
  });
});