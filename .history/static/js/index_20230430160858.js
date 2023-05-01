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

  $(".toast").toast("show");
  $(".toast").toast({
    delay: 2000,
  });

  $("body").on("click", '.close[data-dismiss="toast"]', handleToastAction);
  function handleToastAction() {
    var action = $(this).data("action"),
      dismiss = $(this).data("dismiss");

    if (action === "add") {
      $(".toast-track").prepend(
        renderToast(users[Math.floor(Math.random() * users.length)])
      );
    }

    if (dismiss === "toast") {
      $(this).parents(".toast").remove();
    }
  }
});
