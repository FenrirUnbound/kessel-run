'use strict';

function handleError(err) {
  console.error('Encountered an error while displaying the data');
  console.error(err);
}

function fetchData() {
  return fetch('/api/v1/routes/1/day')
  .then(data => data.json())
  .then(data => data.data.reverse())  // todo: remove reverse operation
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

function convertToMinutes(x) {
  return (parseInt(x,10) / 60).toFixed(2);
}

function graphData([trafficData, routeData]) {
  const g = new Dygraph(
    document.getElementById('graph-container'),
    trafficData,
    {
      axes: {
        y: {
          axisLabelFormatter: convertToMinutes,
          valueFormatter: convertToMinutes
        }
      },
      labels: ['Time'].concat(routeData),
      legend: 'always',
      showRangeSelector: true,
      xlabel: 'Time',
      xValueParser: (x) => (1000 * parseInt(x, 10)),
      ylabel: 'Trip Duration (minutes)'
    });
}

Promise.all([
    fetchData().then(formatData),
    fetchRouteData().then(formatRouteData)
])
.then(graphData)
.catch(handleError);
