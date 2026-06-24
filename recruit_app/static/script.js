function confirmDelete() {
  return confirm("本当に削除しますか？");
}

document.addEventListener("DOMContentLoaded", function () {
  const sortKeySelect = document.getElementById("sort-key");
  const sortOrderSelect = document.getElementById("sort-order");
  const tableBody = document.getElementById("candidate-table-body");

  // 並び替えUIがない画面では何もしない
  if (!sortKeySelect || !sortOrderSelect || !tableBody) {
    return;
  }

  function parseDateValue(value) {
    if (!value) {
      return 0;
    }

    const parsed = Date.parse(value);
    return isNaN(parsed) ? 0 : parsed;
  }

  function compareText(a, b) {
    return a.localeCompare(b, "ja");
  }

  function sortRows() {
    const sortKey = sortKeySelect.value;
    const sortOrder = sortOrderSelect.value;
    const rows = Array.from(tableBody.querySelectorAll("tr"));

    rows.sort(function (rowA, rowB) {
  // アラート優先
  const alertA = Number(rowA.dataset.hasAlert || 0);
  const alertB = Number(rowB.dataset.hasAlert || 0);

  if (alertA !== alertB) {
    return alertB - alertA;
  }

  let valueA;
  let valueB;
  let result = 0;

  if (sortKey === "id") {
    valueA = Number(rowA.dataset.id || 0);
    valueB = Number(rowB.dataset.id || 0);
    result = valueA - valueB;
  } else if (sortKey === "updated_at") {
    valueA = parseDateValue(rowA.dataset.updatedAt);
    valueB = parseDateValue(rowB.dataset.updatedAt);
    result = valueA - valueB;
  } else if (sortKey === "owner") {
    valueA = (rowA.dataset.owner || "").trim();
    valueB = (rowB.dataset.owner || "").trim();
    result = compareText(valueA, valueB);
  } else {
    valueA = (rowA.dataset.name || "").trim();
    valueB = (rowB.dataset.name || "").trim();
    result = compareText(valueA, valueB);
  }

  return sortOrder === "asc" ? result : -result;
  });


    rows.forEach(function (row) {
      tableBody.appendChild(row);
    });
  }

  // セレクト変更で自動反映
  sortKeySelect.addEventListener("change", sortRows);
  sortOrderSelect.addEventListener("change", sortRows);

  // 初期表示時にも現在の選択内容で反映
  sortRows();
});
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
