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
  console.log("Deploying CommitRevealArtParams to Mantle Testnet...");

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
  const artifactsPath = path.join(__dirname, "../artifacts/contracts/CommitRevealArtParams.sol/CommitRevealArtParams.json");
  const artifacts = JSON.parse(fs.readFileSync(artifactsPath, "utf8"));

  // Create contract factory from artifacts
  const factory = new ethers.ContractFactory(artifacts.abi, artifacts.bytecode, wallet);

  // Generate a unique collection salt
  const collectionSalt = ethers.keccak256(ethers.toUtf8Bytes("AleaArt_Collection_2025"));

  console.log("Collection Salt:", collectionSalt);

  // Deploy the contract
  const contract = await factory.deploy(collectionSalt);

  await contract.waitForDeployment();

  const contractAddress = await contract.getAddress();
  console.log("Contract deployed to:", contractAddress);

  // Verify deployment
  console.log("Verifying deployment...");

  // Test basic contract functions
  try {
    const salt = await contract.COLLECTION_SALT();
    console.log("Contract salt:", salt);
    console.log("✅ Contract deployed successfully!");
  } catch (error) {
    console.log("⚠️ Contract verification failed:", error.message);
  }

  console.log("\n🎨 CommitRevealArtParams Deployment successful!");
  console.log("Contract Address:", contractAddress);
  console.log("Network: Mantle Testnet");
  console.log("Collection Salt:", collectionSalt);
  console.log("\n📋 Contract Features:");
  console.log("- Uses commit-reveal mechanism for verifiable randomness");
  console.log("- Generates art parameters from committed secrets");
  console.log("- Creates unique tokens with deterministic parameters");
  console.log("- Supports prompt, style, sampler, aspect ratio, and more");
  console.log("- Prevents front-running with commit phase");
  console.log("- Uses blockhash for additional entropy");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
