var $grid;

$(document).ready(function(){
  $grid = $(".grid").isotope({ "itemSelector": ".country-box", "layoutMode": "fitRows" });
});