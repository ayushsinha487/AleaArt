import type { HardhatUserConfig } from "hardhat/config";
import { configVariable } from "hardhat/config";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.28",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      type: "edr-simulated",
      chainType: "l1",
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      accounts: [""],
    },
    sepolia: {
      type: "http",
      chainType: "l1",
      url: configVariable("SEPOLIA_RPC_URL"),
      accounts: [configVariable("SEPOLIA_PRIVATE_KEY")],
    },
    arbitrumSepolia: {
      type: "http",
      chainType: "l1",
      url: "https://sepolia-rollup.arbitrum.io/rpc",
      accounts: [configVariable("SEPOLIA_PRIVATE_KEY")],
      chainId: 421614,
    },
    mantleTestnet: {
      type: "http",
      chainType: "l1",
      url: "https://rpc.testnet.mantle.xyz",
      accounts: [configVariable("MANTLE_PRIVATE_KEY")],
      chainId: 5001,
    },
  },
};

export default config;
