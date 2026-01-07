// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CommitRevealArtParams {
    // ----------------------------
    // Commit–Reveal RNG
    // ----------------------------
    struct Commit {
        bytes32 hash;
        uint256 blockNumber;
        bool revealed;
    }

    mapping(address => Commit) public commits;

    event Committed(address indexed user);
    event Revealed(address indexed user, uint256 tokenId, bytes32 seed);

    // ----------------------------
    // Art Logic (UNCHANGED)
    // ----------------------------
    bytes32 public immutable COLLECTION_SALT;
    uint256 public nextTokenId = 1;

    mapping(uint256 => bytes32) public tokenSeed;

    struct RenderParams {
        uint8  promptIndex;
        uint8  styleIndex;
        uint8  samplerIndex;
        uint8  aspectIndex;
        uint16 steps;
        uint16 cfg;
        uint32 latentSeed;
        uint16 paletteId;
    }

    mapping(uint256 => RenderParams) internal _params;

    constructor(bytes32 collectionSalt) {
        COLLECTION_SALT = collectionSalt;
    }

    // ----------------------------
    // Step 1. Commit
    // ----------------------------
    function commit(bytes32 hash) external {
        require(commits[msg.sender].hash == bytes32(0), "already committed");
        commits[msg.sender] = Commit({
            hash: hash,
            blockNumber: block.number,
            revealed: false
        });
        emit Committed(msg.sender);
    }

    // ----------------------------
    // Step 2. Reveal + Generate Art
    // ----------------------------
    function reveal(uint256 secret) external returns (uint256 tokenId) {
        Commit storage c = commits[msg.sender];
        require(c.hash != bytes32(0), "no commit");
        require(!c.revealed, "already revealed");
        require(
            keccak256(abi.encodePacked(secret)) == c.hash,
            "invalid secret"
        );

        // 🔑 Final randomness (same pattern you already tested)
        bytes32 seed = keccak256(
            abi.encodePacked(
                secret,
                blockhash(c.blockNumber + 1),
                block.prevrandao,
                msg.sender,
                COLLECTION_SALT
            )
        );

        tokenId = nextTokenId++;
        tokenSeed[tokenId] = seed;
        _params[tokenId] = _deriveParams(seed);

        c.revealed = true;
        delete commits[msg.sender];

        emit Revealed(msg.sender, tokenId, seed);
    }

    // ----------------------------
    // Art Param Derivation (UNCHANGED)
    // ----------------------------
    function _deriveParams(bytes32 seed)
        internal
        pure
        returns (RenderParams memory p)
    {
        uint256 s0 = uint256(seed);
        uint256 s1 = uint256(keccak256(abi.encodePacked(seed, uint256(1))));
        uint256 s2 = uint256(keccak256(abi.encodePacked(seed, uint256(2))));
        uint256 s3 = uint256(keccak256(abi.encodePacked(seed, uint256(3))));

        p.promptIndex  = uint8(s0 % 12);
        p.styleIndex   = uint8((s0 >> 40) % 10);
        p.samplerIndex = uint8((s1 >> 96) % 6);
        p.aspectIndex  = uint8((s1 >> 160) % 5);
        p.paletteId    = uint16((s2 >> 200) % 24);
        p.steps        = uint16(18 + (s2 % 47));   // 18–64
        p.cfg          = uint16(70 + (s3 % 111));  // 7.0–18.0 (×10)
        p.latentSeed   = uint32(s3);
    }

    // ----------------------------
    // View (UNCHANGED)
    // ----------------------------
    function viewRenderParams(uint256 tokenId)
        external
        view
        returns (RenderParams memory)
    {
        require(tokenSeed[tokenId] != bytes32(0), "not ready");
        return _params[tokenId];
    }
}
