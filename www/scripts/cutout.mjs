// 펭귄 3D 렌더(흰 배경)에서 가장자리 흰색만 flood-fill로 제거해 투명 PNG 생성.
// 흰 배(belly)는 파란 몸통에 둘러싸여 가장자리와 연결이 끊겨 보존된다.
import sharp from "sharp";

const SRC =
  "/Users/jangminseok/Downloads/KakaoTalk_Photo_2026-06-11-00-09-40.jpeg";
const OUT = "public/mascot.png";

const { data, info } = await sharp(SRC)
  .ensureAlpha()
  .raw()
  .toBuffer({ resolveWithObject: true });

const { width, height, channels } = info;
const isWhite = (i) =>
  data[i] > 232 && data[i + 1] > 232 && data[i + 2] > 232;

const visited = new Uint8Array(width * height);
const stack = [];
const seed = (x, y) => {
  if (x < 0 || y < 0 || x >= width || y >= height) return;
  stack.push(x, y);
};
for (let x = 0; x < width; x++) {
  seed(x, 0);
  seed(x, height - 1);
}
for (let y = 0; y < height; y++) {
  seed(0, y);
  seed(width - 1, y);
}

while (stack.length) {
  const y = stack.pop();
  const x = stack.pop();
  const p = y * width + x;
  if (visited[p]) continue;
  visited[p] = 1;
  const i = p * channels;
  if (!isWhite(i)) continue; // 경계(파랑/주황 등) → 확산 중지
  data[i + 3] = 0;
  seed(x + 1, y);
  seed(x - 1, y);
  seed(x, y + 1);
  seed(x, y - 1);
}

// 가벼운 페더링: 투명 픽셀과 맞닿은 아주 밝은 픽셀 알파를 낮춰 흰 테두리 완화
const orig = Uint8Array.from(data);
for (let y = 1; y < height - 1; y++) {
  for (let x = 1; x < width - 1; x++) {
    const p = y * width + x;
    const i = p * channels;
    if (orig[i + 3] === 0) continue;
    const veryLight = orig[i] > 224 && orig[i + 1] > 224 && orig[i + 2] > 224;
    if (!veryLight) continue;
    const transNeighbor =
      orig[((y) * width + (x + 1)) * channels + 3] === 0 ||
      orig[((y) * width + (x - 1)) * channels + 3] === 0 ||
      orig[((y + 1) * width + x) * channels + 3] === 0 ||
      orig[((y - 1) * width + x) * channels + 3] === 0;
    if (transNeighbor) data[i + 3] = 90;
  }
}

await sharp(data, { raw: { width, height, channels } })
  .trim()
  .png()
  .toFile(OUT);

console.log(`done: ${OUT} (${width}x${height})`);
