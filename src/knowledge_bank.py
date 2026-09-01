"""
Spec2Verify Knowledge Bank
Contains pre-loaded sample hardware specifications, governing industry standards (AMBA, JEDEC, IEEE, NXP),
and protocol reference snippets for immediate system testing and verification exploration.
"""

SAMPLE_SPECIFICATIONS = {
    "AXI4-Stream FIFO Controller": {
        "domain": "On-Chip Interconnect",
        "standard_ref": "ARM AMBA AXI4-Stream Protocol Specification v1.0",
        "description": "A synchronous FIFO controller managing data streaming with backpressure using TVALID and TREADY handshakes.",
        "requirements": [
            {"req_id": "REQ_AXIS_01", "description": "TVALID must remain asserted until TREADY is sampled high at the positive clock edge.", "category": "Protocol", "priority": "Mandatory"},
            {"req_id": "REQ_AXIS_02", "description": "FIFO overflow flag must assert within 1 clock cycle when write occurs on a full buffer.", "category": "Error Handling", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "Section 3.2: Handshake Process - TVALID and TREADY dependency rules.",
            "Section 4.1: Overflow protection mechanisms in asynchronous clock domains."
        ]
    },
    "APB4 Register Interface": {
        "domain": "Control/Status Registers",
        "standard_ref": "ARM AMBA APB Protocol v2.0",
        "description": "Low-power peripheral bus bridge handling 32-bit register reads and writes with PSEL, PENABLE, and PREADY.",
        "requirements": [
            {"req_id": "REQ_APB_01", "description": "PREADY can be driven LOW to insert wait states during transfer phase.", "category": "Timing", "priority": "Mandatory"},
            {"req_id": "REQ_APB_02", "description": "PSELx and PENABLE must be mutually exclusive during idle state transitions.", "category": "Protocol", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "Section 2.1: APB Operating States (IDLE, SETUP, ACCESS).",
            "Section 2.3: Protection Unit support (PPROT)."
        ]
    },
    "I2C Master Controller": {
        "domain": "Serial Peripheral Interface",
        "standard_ref": "NXP I2C-bus specification and user manual UM10204",
        "description": "Multi-speed I2C master supporting Standard mode (100 kbps), Fast mode (400 kbps), and clock stretching.",
        "requirements": [
            {"req_id": "REQ_I2C_01", "description": "Controller must generate START condition by pulling SDA LOW while SCL is HIGH.", "category": "Timing", "priority": "Mandatory"},
            {"req_id": "REQ_I2C_02", "description": "Clock stretching by slave device must hold SCL LOW and pause internal baud counter.", "category": "Protocol", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "Section 3.1.1: START and STOP conditions generation.",
            "Section 3.1.3: Clock stretching behavior and timeout handling."
        ]
    },
    "SPI Quad Flash Controller": {
        "domain": "Non-Volatile Memory Interface",
        "standard_ref": "JEDEC JESD216 (Serial Flash Discoverable Parameters)",
        "description": "High-throughput Quad SPI controller supporting single, dual, and quad wire read/write commands.",
        "requirements": [
            {"req_id": "REQ_SPI_01", "description": "Chip select (CS_n) must remain asserted for the entire duration of the instruction and data transfer.", "category": "Protocol", "priority": "Mandatory"},
            {"req_id": "REQ_SPI_02", "description": "Data output valid window must meet setup time requirements relative to SCK falling edge.", "category": "Timing", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "JESD216D: Command parsing table for 1-1-4 and 4-4-4 read modes.",
            "Timing Diagram 4: Dual/Quad output transfer constraints."
        ]
    },
    "UART Baud Rate Generator": {
        "domain": "Asynchronous Serial Communication",
        "standard_ref": "Industry Standard 16550 UART",
        "description": "Configurable baud rate generator with 16x oversampling clock and programmable framing bits.",
        "requirements": [
            {"req_id": "REQ_UART_01", "description": "Sampling engine must detect start bit falling edge within 5% error margin across 16x ticks.", "category": "Accuracy", "priority": "Mandatory"},
            {"req_id": "REQ_UART_02", "description": "Parity error interrupt must trigger immediately upon stop bit validation failure.", "category": "Error Handling", "priority": "Desirable"}
        ],
        "reference_snippets": [
            "Section 5.4: Baud rate divisor calculation formulas.",
            "Section 6.2: Framing error detection state machine."
        ]
    },
    "DMA Scatter-Gather Engine": {
        "domain": "System Bus Master",
        "standard_ref": "PCIe Base Specification v4.0 (DMA Subsystem)",
        "description": "Descriptor-based direct memory access controller supporting ring buffers and unaligned transfers.",
        "requirements": [
            {"req_id": "REQ_DMA_01", "description": "Engine shall automatically fetch next descriptor from system memory when current descriptor status sets 'Done'.", "category": "Functional", "priority": "Mandatory"},
            {"req_id": "REQ_DMA_02", "description": "Bus error response on read port must abort current transfer channel and assert error interrupt.", "category": "Error Handling", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "Chapter 7: Ring buffer management and pointer wraparound.",
            "Section 7.4: Error reporting and fault recovery protocols."
        ]
    },
    "Ethernet MAC Frame Filter": {
        "domain": "Networking Interface",
        "standard_ref": "IEEE 802.3-2022 Clause 3 (Media Access Control)",
        "description": "Layer 2 MAC frame filtering block supporting unicast, multicast hash tables, and VLAN tag stripping.",
        "requirements": [
            {"req_id": "REQ_ETH_01", "description": "Frames with invalid Frame Check Sequence (FCS) must be dropped silently without forwarding to RX FIFO.", "category": "Filtering", "priority": "Mandatory"},
            {"req_id": "REQ_ETH_02", "description": "Destination address matching must execute within 2 clock cycles of preamble stripping.", "category": "Performance", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "Clause 3.2: Frame format and CRC32 verification standard.",
            "Clause 5.1: Address filtering hash lookup logic."
        ]
    },
    "DDR4 Memory Controller PHY": {
        "domain": "High-Speed Memory Interface",
        "standard_ref": "JEDEC JESD79-4B (DDR4 SDRAM Specification)",
        "description": "Command and address training interface managing impedance calibration, leveling, and refresh timing.",
        "requirements": [
            {"req_id": "REQ_DDR_01", "description": "Refresh interval (tREFI) violation counter must trigger emergency self-refresh entry.", "category": "Timing", "priority": "Mandatory"},
            {"req_id": "REQ_DDR_02", "description": "Write leveling feedback loop must adjust DQS-DQ skew within 2 picosecond increments.", "category": "Calibration", "priority": "Mandatory"}
        ],
        "reference_snippets": [
            "JESD79-4B Section 4.2: Initialization sequence and mode register programming.",
            "JESD79-4B Section 5.8: Refresh timing parameters and constraints."
        ]
    }
}
