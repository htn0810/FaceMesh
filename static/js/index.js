jQuery(function ($) {
  $(".sidebar-dropdown > a").click(function () {
    $(".sidebar-submenu").slideUp(200);
    if ($(this).parent().hasClass("active")) {
      $(".sidebar-dropdown").removeClass("active");
      $(this).parent().removeClass("active");
    } else {
      $(".sidebar-dropdown").removeClass("active");
      $(this).next(".sidebar-submenu").slideDown(200);
      $(this).parent().addClass("active");
    }
  });

  $("#close-sidebar").click(function () {
    $(".page-wrapper").removeClass("toggled");
  });
  $("#show-sidebar").click(function () {
    $(".page-wrapper").addClass("toggled");
  });

  $(document).ready(function () {
    $(".toast").toast("show");
  });

  $("body").on("click", '.close[data-dismiss="toast"]', handleToastAction);
  function handleToastAction() {
    dismiss = $(this).data("dismiss");

    if (dismiss === "toast") {
      $(this).parents(".toast").remove();
    }
  }
});
