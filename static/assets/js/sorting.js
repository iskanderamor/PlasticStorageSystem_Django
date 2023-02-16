function clearFilters() {
  document.getElementById("date_from").value = "";
  document.getElementById("date_to").value = "";
  }
weight_up = document.getElementById("weight_up");
weight_down = document.getElementById("weight_down");
date_added_up = document.getElementById("date_added_up");
date_added_down = document.getElementById("date_added_down");
weight_up_form = document.getElementById("weight_up_form");
weight_down_form = document.getElementById("weight_down_form");
date_added_up_form = document.getElementById("date_added_up_form");
date_added_down_form = document.getElementById("date_added_down_form");
weight_up.addEventListener("click", (e) => weight_up_form.submit());
weight_down.addEventListener("click", (e) => weight_down_form.submit());
date_added_up.addEventListener("click", (e) => date_added_up_form.submit());
date_added_down.addEventListener("click", (e) => date_added_down_form.submit());
  