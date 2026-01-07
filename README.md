# AleaArt - Blockchain-Powered Generative Art Platform

AleaArt is a decentralized platform that generates unique art parameters using a verifiable on-chain commit-reveal mechanism on Mantle Testnet, creates AI-generated images using Clipdrop API, and enables NFT minting and trading. Each art piece is truly unique, verifiable on the blockchain, and tradeable as NFTs.

## 🎨 Key Features

- **Commit-Reveal RNG**: Verifiable on-chain randomness using a secure two-step commit-reveal protocol
- **Generative Art Parameters**: Converts randomness into detailed art generation parameters
- **AI Image Generation**: Creates stunning images using Clipdrop API
- **NFT Minting**: Convert generated art into tradeable NFTs on Mantle Testnet
- **Decentralized Marketplace**: Buy and sell NFTs directly peer-to-peer
- **IPFS Storage**: Images stored on decentralized IPFS network via Pinata
- **User Authentication**: Secure login/signup with NextAuth.js
- **Wallet Integration**: MetaMask connection for blockchain interactions
- **Image Gallery**: Personal gallery to view and manage generated artwork
- **Real-time Generation**: Asynchronous image generation with status tracking

## 🔗 Smart Contracts

### CommitRevealArtParams Contract
**Address**: `0x01f077E8a758D12B14e07eE72764df963378e001`  
**Network**: Mantle Testnet  
**Location**: `contracts/MantleCommitRevealArtParams.sol`

The core contract that implements a **Commit-Reveal** scheme to generate deterministic art parameters:

- **Commit Phase**: Users commit a hash of a secret to prevent front-running and ensure fairness
- **Reveal Phase**: Users reveal their secret to generate verifiable randomness
- **Parameter Generation**: Converts the resulting seed into art parameters:
  - Prompt templates (12 different styles)
  - Style modifiers (10 artistic styles)
  - Technical parameters (steps, CFG scale, aspect ratio)
  - Unique seeds for reproducibility
- **On-Chain Storage**: Stores parameters permanently for verification

### AleaArtNFT Contract
**Address**: `0x686d373E8feBA2B2De4576771B2045EFEAE574cE`  
**Network**: Mantle Testnet  
**Location**: `contracts/AleaArtNFT.sol`

The NFT marketplace contract enabling art trading:

- **NFT Minting**: Convert generated art into ERC721 NFTs
- **IPFS Integration**: Links NFTs to images stored on IPFS
- **Marketplace Functions**: Buy, sell, and trade NFTs
- **Price Management**: Set and update NFT prices
- **Ownership Tracking**: Tracks both creator and current owner
- **Direct Payments**: 100% of sale proceeds go to seller (no platform fees)
- **Sale Status**: Enable/disable NFTs for sale

### Contract Functions Overview

#### CommitRevealArtParams:
- `commit(bytes32 hash)` - Submit a hash of your secret
- `reveal(uint256 secret)` - Reveal secret to generate parameters and mint token ID
- `viewRenderParams(tokenId)` - View generated parameters
- `tokenSeed(tokenId)` - Get the random seed used
- `nextTokenId()` - Get next available token ID

#### AleaArtNFT:
- `mintNFT(to, ipfsHash, prompt, price)` - Mint new NFT
- `buyNFT(tokenId)` - Purchase NFT (sends ETH to seller)
- `setPrice(tokenId, newPrice)` - Update NFT price
- `setSaleStatus(tokenId, isForSale)` - Enable/disable for sale
- `getAllNFTs()` - Get all minted NFTs
- `getNFTsForSale()` - Get NFTs currently for sale


## 📁 Project Structure

```
AleaArt/
├── contracts/                      # Smart Contracts (Solidity)
│   ├── AleaArtNFT.sol             # NFT marketplace and trading
│   └── CommitRevealArtParams.sol  # Commit-reveal mechanism for art parameters
│
├── frontend-aleart/                # Frontend Application (Next.js)
│   ├── src/
│   │   ├── app/                    # Next.js app router pages
│   │   │   ├── page.tsx           # Landing page
│   │   │   ├── marketplace/       # NFT marketplace page
│   │   │   ├── dashboard/         # User dashboard for generation
│   │   │   └── api/               # API routes
│   │   │       ├── buy-nft/       # NFT purchase endpoint
│   │   │       ├── marketplace/   # Market data endpoint
│   │   │       └── ...
│   │   ├── components/            # React components
│   │   ├── lib/                   # Utilities (auth, db)
│   │   ├── models/                # MongoDB models
│   │   └── types/                 # TypeScript types
│   ├── public/                    # Static assets
│   └── package.json               # Node.js dependencies
│
├── python_backend.py              # Flask backend for Stable Diffusion
├── python_backend_macos.py        # macOS-specific backend
├── python_backend_simple.py       # Simplified backend version (deprecated)
├── python_backend_clipdrop.py     # Flask backend using Clipdrop API
├── test_async_api.py              # Async API testing
│
├── scripts/                       # Deployment scripts
│   ├── deploy-artParams.ts        # Deploy art params contract
│   └── deploy-nft-arbitrum.ts    # Deploy NFT contract
│
├── generated_images/               # Generated artwork storage (local)
├── artifacts/                     # Compiled contract artifacts
├── cache/                         # Build cache
├── hardhat.config.ts              # Hardhat configuration
│
├── requirements.txt               # Python dependencies
├── requirements_macos.txt         # macOS Python dependencies
├── package.json                   # Root node.js dependencies
└── README.md                       # This file
```

### Directory Overview

- **`contracts/`** - Solidity smart contracts that handle on-chain logic, NFT minting, trading, and randomness
- **`frontend-aleart/`** - Next.js frontend application with TypeScript, Tailwind CSS, and React components
- **`python_backend*.py`** - Python Flask servers for AI image generation (Stable Diffusion or Clipdrop API)
- **`scripts/`** - Hardhat deployment scripts for deploying contracts
- **`generated_images/`** - Local storage for generated artwork before IPFS upload
- **`artifacts/`** - Compiled contract artifacts and build information

## 🏗️ Architecture

- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **Backend**: Python Flask with Stable Diffusion integration
- **Database**: MongoDB for user data and generated images metadata
- **Blockchain**: Mantle Testnet
- **Authentication**: NextAuth.js with JWT tokens
- **Image Storage**: IPFS via Pinata (decentralized)
- **NFT Standard**: ERC721 compliant
- **Payment**: Direct ETH transfers (no platform fees)

## 🚀 Technology Stack

- **Blockchain**: Solidity, Hardhat, Ethers.js, OpenZeppelin
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: Python, Flask, Stable Diffusion / Clipdrop API
- **Database**: MongoDB, Mongoose
- **Authentication**: NextAuth.js
- **Storage**: IPFS, Pinata API
- **NFT**: ERC721 standard

## 🔧 Backend Options

### Clipdrop API Backend (Recommended)

The project now supports **Clipdrop API** for faster, cloud-based image generation:

**Features:**
- ⚡ **Faster Generation**: Cloud-based API, no local GPU required
- 🎨 **High Quality**: Professional-grade AI image generation
- 💰 **Cost Effective**: Pay-per-use pricing
- 🚀 **Easy Setup**: No complex model downloads or GPU setup


### Stable Diffusion Backend (Legacy)

The original Stable Diffusion backends are still available but require significant computational resources:

- `python_backend_simple.py` - Basic CPU/GPU support
- `python_backend_macos.py` - macOS optimized
- `python_backend.py` - Full-featured with optimizations

## 🎯 User Journey

1. **Connect Wallet**: Link MetaMask to Mantle Testnet
2. **Commit Secret**: Submit a hashed secret to the contract
3. **Reveal Art Parameters**: Reveal your secret to generate verifiable art parameters
4. **Create Art**: AI generates unique image using Clipdrop API
5. **Mint NFT**: Convert art to tradeable NFT with custom price
6. **Trade**: Buy/sell NFTs in the decentralized marketplace
7. **Own**: Full ownership and control of your digital art


