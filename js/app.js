var $quicksearch;
var qsRegex;
var $grid;

function debounce( fn, threshold ) {
  var timeout;
  return function debounced() {
    if ( timeout ) {
      clearTimeout( timeout );
    }
    function delayed() {
      fn();
      timeout = null;
    }
    timeout = setTimeout( delayed, threshold || 100 );
  }
}

$(document).ready(function(){
  $grid = $(".grid").isotope({ 
    itemSelector: ".country-box", 
    layoutMode: "fitRows",
    filter: function() {
      return qsRegex ? $(this).text().match( qsRegex ) : true;
    } 
  });

  // use value of search field to filter
  $quicksearch = $('.quicksearch').keyup( debounce( function() {
    qsRegex = new RegExp( $quicksearch.val(), 'gi' );
    $grid.isotope();
  }, 200 ) );

});