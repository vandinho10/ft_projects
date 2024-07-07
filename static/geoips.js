function geoFindMe() {
    const status = document.querySelector("#status");
    const latitudeInput = document.querySelector("#latitude");
    const longitudeInput = document.querySelector("#longitude");

    function success(position) {
        const latitude = position.coords.latitude.toFixed(6);
        const longitude = position.coords.longitude.toFixed(6);
        const accuracy = position.coords.accuracy.toFixed(2);

        status.textContent = ` - Localizando… - Precisão: ${accuracy} metros`;

        if (accuracy <= 6) {
            status.textContent = ` - Precisão: ${accuracy} metros`;
            latitudeInput.value = latitude;
            longitudeInput.value = longitude;
            navigator.geolocation.clearWatch(watchId);
        }
    }

    function error() {
        status.textContent = " - Não foi possível obter sua localização";
    }

    if (!navigator.geolocation) {
        status.textContent = " - Geolocalização não é suportada pelo seu navegador";
    } else {
        status.textContent = " - Localizando…";
        var watchId = navigator.geolocation.watchPosition(success, error, { enableHighAccuracy: true });
    }
}

document.querySelector("#insert-coordinates").addEventListener("click", geoFindMe);
