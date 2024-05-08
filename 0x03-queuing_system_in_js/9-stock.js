import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const PORT = 1245;

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

const getItemById = (id) => {
  return listProducts.find(product => product.itemId === id);
};

const reserveStockById = (itemId, stock) => {
  return promisify(client.set).bind(client)(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const getAsync = promisify(client.get).bind(client);
  const reservedStock = await getAsync(`item.${itemId}`);
  return parseInt(reservedStock) || 0;
};

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  const currentQuantity = product.initialAvailableQuantity - await getCurrentReservedStockById(itemId);
  res.json({ ...product, currentQuantity });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  const currentStock = product.initialAvailableQuantity - await getCurrentReservedStockById(itemId);
  if (currentStock <= 0) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }
  let reserved = await getCurrentReservedStockById(itemId);
  await reserveStockById(itemId, reserved + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
