fetch('/api/stations-list')
    .then(response => {
        if (!response.ok) {
            throw new Error('РћС€РёР±РєР° Р·Р°РіСЂСѓР·РєРё СЃС‚Р°РЅС†РёР№');
        }
        return response.json();
    })
    .then(apiStations => {
        const container = document.getElementById('stations-container');
        container.innerHTML = ''; 
        
        apiStations.forEach(station => {
            const data = stationsData[station.id];
            if (!data) {
                console.warn(`РќРµС‚ РєРѕРѕСЂРґРёРЅР°С‚ РґР»СЏ СЃС‚Р°РЅС†РёРё ID ${station.id} (${station.name})`);
                return;
            }
            
            const pos = data.pos;
            const line = data.line;
            
            const stationDiv = document.createElement('div');
            stationDiv.className = 'station';
            stationDiv.style.top = pos.top + 'px';
            stationDiv.style.left = pos.left + 'px';

            const link = document.createElement('a');
            link.href = `/station/${station.id}`;
            link.className = `station-button ${line}`;
            link.textContent = station.name;
            
            stationDiv.appendChild(link);
            container.appendChild(stationDiv);
        });
    })
    .catch(error => {
        console.error('РћС€РёР±РєР°:', error);
        document.getElementById('stations-container').innerHTML = 
            '<div style="color: red; padding: 20px;">РћС€РёР±РєР° Р·Р°РіСЂСѓР·РєРё СЃС‚Р°РЅС†РёР№</div>';
    });