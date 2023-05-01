// All Records table use this
$(document).ready(function(){
  $('#dataTable').DataTable({
    order: [[0, 'asc']],
    'aoColumnDefs':[{
      'bSortable': false,
      'aTargets': ['nosort']
    }]
  });



  // Remove Record table
  $('#removeDataTable').DataTable({
    order: [[1, 'asc']],
    'aoColumnDefs':[{
      'bSortable': false,
      'aTargets': ['nosort']
    }]
  });

  // Bin Category Modal
  $('#binCategoryDataTable').DataTable({
    order: [[0, 'asc']],
    'aoColumnDefs':[{
      'bSortable': false,
      'aTargets': ['nosort']
    }]
  });

  // Bin Brands Modal
  $('#binBrandsDataTable').DataTable({
    order: [[0, 'asc']],
    'aoColumnDefs':[{
      'bSortable': false,
      'aTargets': ['nosort']
    }]
  });

  // Products Brands Modal
  $('#binProductsDataTable').DataTable({
    order: [[0, 'asc']],
    'aoColumnDefs':[{
      'bSortable': false,
      'aTargets': ['nosort']
    }]
  });
  
  // Employees Brands Modal
  $('#binEmpDataTable').DataTable({
    order: [[0, 'asc']],
    'aoColumnDefs':[{
      'bSortable': false,
      'aTargets': ['nosort']
    }]
  });
});



