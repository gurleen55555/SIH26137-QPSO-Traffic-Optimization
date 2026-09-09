import React, { useEffect, useRef, useState } from 'react'
import { MapContainer, TileLayer, Polyline as LeafletPolyline, CircleMarker, Popup as LeafletPopup, useMap } from 'react-leaflet'
import { useJsApiLoader, GoogleMap, Polyline as GooglePolyline, Marker as GoogleMarker, InfoWindow } from '@react-google-maps/api'

const VEHICLE_COLORS = ['#00e5ff', '#ffb300', '#00e676', '#d500f9', '#ff6e40']
const CENTER = { lat: 12.9716, lng: 77.5946 }
const DARK_TILE = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'

const GOOGLE_MAP_DARK_STYLES = [
  { elementType: 'geometry', stylers: [{ color: '#0d1322' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#7488a1' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#0d1322' }] },
  { featureType: 'administrative', elementType: 'geometry', stylers: [{ color: '#1e293b' }] },
  { featureType: 'poi', elementType: 'labels.text.fill', stylers: [{ color: '#64748b' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#1e293b' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#0f172a' }] },
  { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#334155' }] },
  { featureType: 'road.highway', elementType: 'geometry.stroke', stylers: [{ color: '#1e293b' }] },
  { featureType: 'transit', elementType: 'geometry', stylers: [{ color: '#1e293b' }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#080e1a' }] },
]

function LeafletFitBounds({ bounds }) {
  const map = useMap()
  useEffect(() => {
    if (bounds && bounds.length >= 2) {
      map.fitBounds(bounds, { padding: [30, 30] })
    }
  }, [bounds, map])
  return null
}

export default function MapCanvas({
  graphData,
  routes,
  mapProvider = 'google',
  apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '',
}) {
  const [activeMarker, setActiveMarker] = useState(null)
  const nodePositions = useRef({})

  // Compute node positions
  useEffect(() => {
    if (!graphData?.features) return
    const positions = {}
    for (const f of graphData.features) {
      if (f.geometry.type === 'Point') {
        const [lon, lat] = f.geometry.coordinates
        positions[f.properties.node_id] = { lat, lng: lon }
      }
    }
    nodePositions.current = positions
  }, [graphData])

  // Build edge lines
  const edgeLines = []
  if (graphData?.features) {
    for (const f of graphData.features) {
      if (f.geometry.type === 'LineString') {
        const coords = f.geometry.coordinates.map(([lon, lat]) => ({ lat, lng: lon }))
        const congestion = f.properties.congestion || 0
        edgeLines.push({ coords, congestion })
      }
    }
  }

  // Build route lines
  const routeLines = []
  if (routes?.vehicles) {
    routes.vehicles.forEach((vehicle, idx) => {
      if (!vehicle.route_node_ids?.length) return
      const positions = vehicle.route_node_ids
        .map((id) => nodePositions.current[id])
        .filter(Boolean)
      if (positions.length > 0) {
        routeLines.push({
          positions,
          color: VEHICLE_COLORS[idx % VEHICLE_COLORS.length],
          vehicleId: vehicle.vehicle_id,
          distance: vehicle.route_distance_m,
          time: vehicle.route_time_s,
        })
      }
    })
  }

  // Google Maps JS API loader
  const { isLoaded, loadError } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: apiKey,
  })

  const useGoogleMap = mapProvider === 'google' && apiKey && isLoaded && !loadError

  // Render Google Maps view
  if (useGoogleMap) {
    return (
      <GoogleMap
        mapContainerStyle={{ width: '100%', height: '100%' }}
        center={CENTER}
        zoom={14}
        options={{
          styles: GOOGLE_MAP_DARK_STYLES,
          disableDefaultUI: false,
          zoomControl: true,
          mapTypeControl: true,
        }}
      >
        {/* Network Edges */}
        {edgeLines.map((edge, i) => (
          <GooglePolyline
            key={`g-edge-${i}`}
            path={edge.coords}
            options={{
              strokeColor: edge.congestion > 0.5 ? '#ff1744' : edge.congestion > 0.2 ? '#ffb300' : '#334155',
              strokeOpacity: 0.5,
              strokeWeight: 2,
            }}
          />
        ))}

        {/* Optimized Vehicle Routes */}
        {routeLines.map((route, i) => (
          <React.Fragment key={`g-route-${i}`}>
            <GooglePolyline
              path={route.positions}
              options={{
                strokeColor: route.color,
                strokeOpacity: 0.9,
                strokeWeight: 5,
              }}
            />
            {/* Route Markers */}
            {route.positions.map((pos, pIdx) => (
              <GoogleMarker
                key={`g-dest-${i}-${pIdx}`}
                position={pos}
                label={{
                  text: `${pIdx === 0 ? 'D' : pIdx}`,
                  color: '#000000',
                  fontWeight: 'bold',
                  fontSize: '11px',
                }}
                onClick={() => setActiveMarker({ pos, text: `Stop ${pIdx + 1} — Vehicle V${route.vehicleId}` })}
              />
            ))}
          </React.Fragment>
        ))}

        {activeMarker && (
          <InfoWindow
            position={activeMarker.pos}
            onCloseClick={() => setActiveMarker(null)}
          >
            <div style={{ color: '#000', padding: '4px', fontWeight: 'bold' }}>
              {activeMarker.text}
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    )
  }

  // Fallback: Leaflet Dark Map View
  const leafletBounds = []
  edgeLines.forEach((e) => e.coords.forEach((c) => leafletBounds.push([c.lat, c.lng])))
  routeLines.forEach((r) => r.positions.forEach((p) => leafletBounds.push([p.lat, p.lng])))

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {mapProvider === 'google' && !apiKey && (
        <div
          style={{
            position: 'absolute',
            top: 10,
            left: 10,
            zIndex: 1000,
            background: 'rgba(15, 23, 42, 0.9)',
            border: '1px solid var(--accent-amber)',
            color: 'var(--accent-amber)',
            padding: '6px 12px',
            borderRadius: '8px',
            fontSize: '0.75rem',
            pointerEvents: 'none',
          }}
        >
          💡 Using Dark Leaflet map. Add Google Maps API Key in control panel to switch to Google Maps.
        </div>
      )}

      <MapContainer center={[CENTER.lat, CENTER.lng]} zoom={14} style={{ height: '100%', width: '100%' }}>
        <TileLayer attribution='&copy; <a href="https://carto.com/">CARTO</a>' url={DARK_TILE} />

        {leafletBounds.length >= 2 && <LeafletFitBounds bounds={leafletBounds} />}

        {/* Network Edges */}
        {edgeLines.map((edge, i) => (
          <LeafletPolyline
            key={`edge-${i}`}
            positions={edge.coords.map((c) => [c.lat, c.lng])}
            pathOptions={{
              color: edge.congestion > 0.5 ? '#ff1744' : edge.congestion > 0.2 ? '#ffb300' : '#334155',
              weight: 1.5,
              opacity: 0.4,
            }}
          />
        ))}

        {/* Vehicle Routes */}
        {routeLines.map((route, i) => (
          <LeafletPolyline
            key={`route-${i}`}
            positions={route.positions.map((p) => [p.lat, p.lng])}
            pathOptions={{
              color: route.color,
              weight: 4,
              opacity: 0.9,
            }}
          >
            <LeafletPopup>
              <strong>Vehicle V{route.vehicleId}</strong><br />
              Distance: {(route.distance / 1000).toFixed(2)} km<br />
              Time: {(route.time / 60).toFixed(1)} min
            </LeafletPopup>
          </LeafletPolyline>
        ))}

        {/* Delivery Stop Markers */}
        {routeLines.flatMap((route, rIdx) =>
          route.positions.map((pos, pIdx) => (
            <CircleMarker
              key={`dest-${rIdx}-${pIdx}`}
              center={[pos.lat, pos.lng]}
              radius={6}
              pathOptions={{
                fillColor: route.color,
                fillOpacity: 0.9,
                color: '#fff',
                weight: 2,
              }}
            >
              <LeafletPopup>
                Stop {pIdx + 1} — Vehicle V{route.vehicleId}
              </LeafletPopup>
            </CircleMarker>
          ))
        )}
      </MapContainer>
    </div>
  )
}
