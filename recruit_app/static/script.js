function confirmDelete() {
  return confirm("本当に削除しますか？");
}

//function confirmDelete() {
//return confirm("本当に削除しますか？");
//}


// document.addEventListener("DOMContentLoaded", function () {
//   const container = document.getElementById("popup-alert-container");

//   // 通知コンテナがない画面では何もしない
//   if (!container) {
//     return;
//   }

//   // クリック処理（イベント委譲）
//   container.addEventListener("click", function (event) {
//     const closeBtn = event.target.closest(".popup-close-btn");

//     // × ボタンが押された場合
//     if (closeBtn) {
//       event.stopPropagation();

//       const popup = closeBtn.closest(".popup-alert");
//       if (!popup) {
//         return;
//       }

//       // localStorage には保存しない
//       // その場だけ消す
//       popup.remove();
//       return;
//     }

//     // 通知本体が押された場合
//     const popup = event.target.closest(".popup-alert");
//     if (popup) {
//       const detailUrl = popup.dataset.detailUrl;
//       if (detailUrl) {
//         window.location.href = detailUrl;
//       }
//     }
//   });
// });


//   // クリック処理（イベント委譲）
//   container.addEventListener("click", function (event) {
//     const closeBtn = event.target.closest(".popup-close-btn");

//     // × ボタンが押された場合
//     if (closeBtn) {
//       event.stopPropagation();

//       const popup = closeBtn.closest(".popup-alert");
//       if (!popup) {
//         return;
//       }

//       const alertId = popup.dataset.alertId;
//       localStorage.setItem("dismissed_" + alertId, "true");
//       popup.remove();
//       return;
//     }

//     // 通知本体が押された場合
//     const popup = event.target.closest(".popup-alert");
//     if (popup) {
//       const detailUrl = popup.dataset.detailUrl;
//       if (detailUrl) {
//         window.location.href = detailUrl;
//       }
//     }
//   });


//その他入力欄　new.html
document.addEventListener("DOMContentLoaded", function () {
  const contactStatus = document.getElementById("contactStatus");
  const contactMemoArea = document.getElementById("contactMemoArea");
  const contactMemo = document.getElementById("contactMemo");

  if (!contactStatus || !contactMemoArea || !contactMemo) {
    return;
  }

  function toggleContactMemo() {
    if (contactStatus.value === "その他") {
      contactMemoArea.style.display = "block";
    } else {
      contactMemoArea.style.display = "none";
      contactMemo.value = "";
    }
  }

  toggleContactMemo();

  contactStatus.addEventListener("change", toggleContactMemo);
});
