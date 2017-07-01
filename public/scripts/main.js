'use strict';

function fetchData() {
  return fetch('/api/v1/routes/1/day')
  .then(data => data.json())
  .then(data => data.data);
}

function fetchRouteData() {
  return fetch('/api/v1/routes')
  .then(data => data.json())
  .then(data => data.data);
}

function formatData(data) {
  return data.map((datapoint) => {
    const timestamp = new Date(datapoint.timestamp * 1000);

    return [
      timestamp,
      datapoint.duration
    ];
  });
}

function formatRouteData(routeData) {
  return routeData.map((item) => {
    return item.name;
  });
}

function graphData([trafficData, routeData]) {
  const g = new Dygraph(
    document.getElementById('graphdiv'),
    trafficData,
    {
      labels: ['Time'].concat(routeData),
      legend: 'always'
    });
}

Promise.all([
    fetchData().then(formatData),
    fetchRouteData().then(formatRouteData)
])
.then(graphData);
