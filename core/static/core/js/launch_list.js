document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const sortSelect = document.getElementById('sortSelect');
  const tableBody = document.querySelector('.launch-table tbody');
  const allRows = Array.from(tableBody.querySelectorAll('tr')).filter(row => row.dataset.id); // Ignora a linha "Nenhum lançamento"

  function filterAndSort() {
    const query = searchInput.value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    let filteredRows = allRows.filter(row => {
      const launchText = row.querySelector('td')?.textContent.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "") || '';
      return launchText.includes(query);
    });


    const sortValue = sortSelect.value;
    filteredRows.sort((a, b) => {
      if (sortValue === 'mais-recente') {
        return new Date(b.dataset.data) - new Date(a.dataset.data);
      }
      if (sortValue === 'mais-antigo') {
        return new Date(a.dataset.data) - new Date(b.dataset.data);
      }
      if (sortValue === 'maior-altura') {
        return parseFloat(b.dataset.altura) - parseFloat(a.dataset.altura);
      }
      return 0;
    });

    tableBody.innerHTML = '';
    filteredRows.forEach(row => tableBody.appendChild(row));

    // Mostra ou esconde mensagem de "nenhum lançamento"
    const noResultsRow = document.querySelector('.no-launches-state');
    if (filteredRows.length === 0) {
      noResultsRow.style.display = 'block';
    } else {
      noResultsRow.style.display = 'none';
    }
  }

  searchInput.addEventListener('input', filterAndSort);
  sortSelect.addEventListener('change', filterAndSort);
});
