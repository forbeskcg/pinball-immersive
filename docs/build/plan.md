# Build Plan

``` mermaid
flowchart TB
    S@{ shape: f-circ, label: "Junction" }
    A1(A1: Whitewood base assembly)
    A2(A2: Mechanism Prototyping)
    A3(A3: Playfield Testing/Refining)
    A4(A4: Transfer Whitewood to CAD)
    A5(A5: Route Final Playfield)
    A6(A6: Fabricate and Install Inserts)
    A7(A7: Artwork)
    A8(A8: Transfer Mechanisms)
    A9(A9: Final Playtesting)
    A10(A10: Install Playfield)

    B1(B1: Assemble Box)
    B2(B2: Mount Monitor)
    B3(B3: Assemble Lower Panel)
    B4(B4: Install Fan)
    B5(B5: Install Lower Panel)
    B6(B6: Wire Everything)
    B7(B7: Install Upper Panel Cover)
    B8(B8: Test Components)
    B9(B9: Attach to Cabinet)
    B10(B10: Paint / Artwork)

    C1(C1: Assemble Box)
        click C1 "../cabinet#assemble-box"
    C2(C2: Attach Legs)
        click C2 "../cabinet#attach-legs"
    C3(C3: Install Glass Rails/Protectors)
        click C3 "../cabinet#install-glass-rails-protectors"
    C4(C4: Electronics)
        click C4 "../cabinet#electronics"
    C4.1(C4.1: External Buttons)
        click C4.1 "../cabinet#external-buttons"
    C4.2(C4.2: Power Strip)
        click C4.2 "../cabinet#power-strip"
    C4.3(C4.3: PC)
        click C4.3 "../cabinet#pc"
    C4.4(C4.4: Audio Components)
        click C4.4 "../cabinet#audio-components"
    C4.5(C4.5: 48v Power Supply)
        click C4.5 "../cabinet#48v-power-supply"
    C5(C5: Attach Backbox)
        click C5 "../cabinet#attach-backbox"
    C6(C6: Painting / Artwork)
        click C6 "../cabinet#painting-artwork"
    C7(C7: Install Playfield)
        click C7 "../cabinet#install-playfield"

%% Provisioning includes setting IDs and deploying base code w/ communication framework
    D1(D1: Provision Boards)
    D2(D2: Setup PC Software)
    D3(D3: Main Game Logic)
    D4(D4: Side quest Logic)
    D5(D5: Light Shows)
    D6(D6: Scores and Visuals)
    D7(D7: Sound effects)
    D8(D8: Configure Kiosk mode)

    subgraph A[Playfield]
        direction TB
        A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7 --> A8 --> A9 --> A10
    end
    subgraph B[Backbox]
        direction TB
        B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> B7 --> B8 --> B9 --> B10
    end
    subgraph C[Cabinet]
        direction TB
        C1 --> C2 --> C3 --> C4 --> C4.1 --> C4.2 --> C4.3 --> C4.4 --> C4.5
        C4.5 --> C5 --> C6 --> C7
    end
    subgraph D[Software]
        direction TB
        D1 --> D2 --> D3 --> D4 --> D5 --> D6 --> D7 --> D8
    end

    E("Playtest!")
    
    S --> A & B & C & D --> E
    
```
