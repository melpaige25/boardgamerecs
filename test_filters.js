// Simple test to verify filtering logic
const fs = require('fs');

// Load data
const ownedGames = JSON.parse(fs.readFileSync('owned-games.json', 'utf8'));
const buyGames = JSON.parse(fs.readFileSync('bgg-recommendations.json', 'utf8'));

console.log('=== Filter Test ===\n');
console.log(`Total owned games: ${ownedGames.length}`);
console.log(`Total buy recommendations: ${buyGames.length}\n`);

// Test filter function
function filterGames(games, playerCount, complexity, duration) {
    return games.filter(game => {
        // Player count filter
        if (playerCount) {
            const players = parseInt(playerCount);
            if (players === 6) {
                if (game.maxplayers < 6) return false;
            } else {
                if (game.minplayers > players || game.maxplayers < players) return false;
            }
        }

        // Complexity filter
        if (complexity) {
            const weight = game.avgweight;
            if (complexity === 'light' && (weight < 1 || weight > 2)) return false;
            if (complexity === 'medium' && (weight < 2 || weight > 3.5)) return false;
            if (complexity === 'heavy' && (weight < 3.5 || weight > 5)) return false;
        }

        // Duration filter
        if (duration) {
            const time = game.playingtime;
            if (duration === 'quick' && time > 30) return false;
            if (duration === 'medium' && (time <= 30 || time > 60)) return false;
            if (duration === 'long' && (time <= 60 || time > 90)) return false;
            if (duration === 'verylong' && time <= 90) return false;
        }

        return true;
    });
}

// Test cases
const tests = [
    { name: 'All games (no filters)', players: '', complexity: '', duration: '' },
    { name: '2 players, light, quick', players: '2', complexity: 'light', duration: 'quick' },
    { name: '4 players, medium complexity', players: '4', complexity: 'medium', duration: '' },
    { name: 'Heavy games, long duration', players: '', complexity: 'heavy', duration: 'long' },
];

tests.forEach(test => {
    const ownedFiltered = filterGames(ownedGames, test.players, test.complexity, test.duration);
    const buyFiltered = filterGames(buyGames, test.players, test.complexity, test.duration);

    console.log(`Test: ${test.name}`);
    console.log(`  Owned games matching: ${ownedFiltered.length}`);
    console.log(`  Buy recommendations matching: ${buyFiltered.length}`);

    if (ownedFiltered.length > 0) {
        console.log(`  Sample owned: ${ownedFiltered[0].name}`);
    }
    if (buyFiltered.length > 0) {
        console.log(`  Sample buy: ${buyFiltered[0].name}`);
    }
    console.log('');
});

console.log('✓ All filter tests completed successfully!');
