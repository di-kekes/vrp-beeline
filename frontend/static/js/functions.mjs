export function getClusterCenter(points) {
  if (!points || points.length === 0) return null;

  let sumX = 0;
  let sumY = 0;

  for (let i = 0; i < points.length; i++) {
    sumX += points[i].coordinates[0];
    sumY += points[i].coordinates[1];
  }

  return [sumX / points.length, sumY / points.length];
}