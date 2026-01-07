import * as dotenv from "dotenv";
import { ethers } from "ethers";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Load environment variables
dotenv.config();

// Fix __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  console.log("Deploying AleaArt NFT Contract to Mantle Testnet...");

  // Check environment variables
  if (!process.env.MANTLE_RPC_URL) {
    throw new Error("MANTLE_RPC_URL not set in environment variables");
  }
  if (!process.env.MANTLE_PRIVATE_KEY) {
    throw new Error("MANTLE_PRIVATE_KEY not set in environment variables");
  }

  // Connect to Mantle Testnet network
  const provider = new ethers.JsonRpcProvider(process.env.MANTLE_RPC_URL);

  // Ensure private key has 0x prefix
  const privateKey = process.env.MANTLE_PRIVATE_KEY.startsWith('0x')
    ? process.env.MANTLE_PRIVATE_KEY
    : '0x' + process.env.MANTLE_PRIVATE_KEY;

  const wallet = new ethers.Wallet(privateKey, provider);

  console.log("Deploying from address:", wallet.address);

  // Read compiled contract artifacts
  const artifactsPath = path.join(__dirname, "../artifacts/contracts/AleaArtNFT.sol/AleaArtNFT.json");
  const artifacts = JSON.parse(fs.readFileSync(artifactsPath, "utf8"));

  // Create contract factory from artifacts
  const factory = new ethers.ContractFactory(artifacts.abi, artifacts.bytecode, wallet);

  // Deploy the contract
  const contract = await factory.deploy();

  await contract.waitForDeployment();

  const contractAddress = await contract.getAddress();
  console.log("✅ Contract deployed to:", contractAddress);

  // Verify deployment
  console.log("Verifying deployment...");

  try {
    const name = await contract.name();
    const symbol = await contract.symbol();
    console.log("Contract name:", name);
    console.log("Contract symbol:", symbol);
    console.log("✅ Contract deployed successfully!");
  } catch (error) {
    console.log("⚠️ Contract verification failed:", error.message);
  }

  console.log("\n🎨 AleaArtNFT Deployment successful!");
  console.log("Contract Address:", contractAddress);
  console.log("Network: Mantle Testnet");
  console.log("\n📋 Contract Features:");
  console.log("- ERC721 compliant NFT marketplace");
  console.log("- IPFS integration for artwork storage");
  console.log("- Direct peer-to-peer trading");
  console.log("- Price management and sale status");
  console.log("- Creator and owner tracking");
  console.log("- No platform fees on transactions");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

