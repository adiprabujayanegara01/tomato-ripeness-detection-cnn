document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector("input[type='file']");
    const previewContainer = document.createElement("div");
    previewContainer.classList.add("text-center", "mt-3");
    fileInput.parentNode.appendChild(previewContainer);

    const label = document.createElement("p");
    label.classList.add("mt-2", "fw-bold");
    label.innerText = "Pilih file gambar";
    fileInput.parentNode.appendChild(label);

    fileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        const predictionStatus = document.getElementById("prediction-status");

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewContainer.innerHTML = `
                    <div class="preview-wrapper">
                        <img src="${e.target.result}" class="img-fluid rounded shadow-sm preview-img" width="200">
                    </div>`;

                const imgElement = previewContainer.querySelector(".preview-img");
                imgElement.addEventListener("mouseenter", () => imgElement.style.transform = "scale(1.1)");
                imgElement.addEventListener("mouseleave", () => imgElement.style.transform = "scale(1)");
            };
            reader.readAsDataURL(file);

            label.innerText = `File dipilih: ${file.name}`;
            label.style.color = "#28a745";

            // Update status prediksi
            predictionStatus.innerHTML = "File dipilih. Silakan klik 'Upload & Prediksi'";
        } else {
            previewContainer.innerHTML = "";
            label.innerText = "Pilih file gambar";
            label.style.color = "#000";
            predictionStatus.innerHTML = "Menunggu upload gambar...";
        }
    });
});

function showLoading() {
    document.getElementById("prediction-status").innerHTML = "⏳ Memproses gambar... Mohon tunggu.";
}
function toggleMenu() {
    var sidebar = document.getElementById("sidebar");
    var menuButton = document.getElementById("menuButton");
    if (sidebar.classList.contains("show")) {
        sidebar.classList.remove("show");
    } else {
        sidebar.classList.add("show");
    }
}
function openCamera() {
    let video = document.getElementById("camera");
    let captureButton = document.getElementById("capture");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
            video.classList.remove("d-none");
            captureButton.classList.remove("d-none");

            // Simpan stream agar bisa dihentikan nanti
            video.dataset.streamId = stream.id;
        })
        .catch(function (err) {
            alert("Akses kamera ditolak atau tidak tersedia");
        });
}
function captureImage() {
    let video = document.getElementById("camera");
    let canvas = document.getElementById("canvas");
    let context = canvas.getContext("2d");
    let takePhotoButton = document.getElementById("takePhotoButton");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Hentikan kamera setelah mengambil gambar
    let stream = video.srcObject;
    let tracks = stream.getTracks();
    tracks.forEach(track => track.stop());

    // Sembunyikan video dan tombol setelah menangkap gambar
    video.classList.add("d-none");
    document.getElementById("capture").classList.add("d-none");
    takePhotoButton.classList.add("d-none");

    // Menampilkan pratinjau gambar di dalam card
    let imgPreview = document.createElement("img");
    imgPreview.src = canvas.toDataURL("image/jpeg");
    imgPreview.classList.add("img-fluid", "rounded", "shadow-sm", "mt-3");
    imgPreview.width = 300;

    let resultDiv = document.createElement("div");
    resultDiv.classList.add("text-center");
    resultDiv.appendChild(imgPreview);

    document.querySelector(".card.shadow-lg").appendChild(resultDiv);

    // Konversi canvas ke file dan set sebagai input file untuk upload
    canvas.toBlob(function (blob) {
        let file = new File([blob], "captured_tomato.jpg", { type: "image/jpeg" });
        let dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.querySelector("input[type=file]").files = dataTransfer.files;
    });
}