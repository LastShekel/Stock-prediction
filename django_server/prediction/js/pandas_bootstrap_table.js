$(function() {
  $('#datatable')({
    striped: true,
    pagination: true,
    showColumns: true,
    showToggle: true,
    showExport: true,
    sortable: true,
    paginationVAlign: 'both',
    pageSize: 25,
    pageList: [10, 25, 50, 100, 'ALL'],
    columns: {{ columns|safe }},  // here is where we use the column content from our Django View
    data: {{ data|safe }}, // here is where we use the data content from our Django View. we escape the content with the safe tag so the raw JSON isn't shown.
  });
});