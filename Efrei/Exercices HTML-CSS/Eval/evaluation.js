// Exercice 2
let title = document.getElementById('title');

title.addEventListener('mouseover', function( event ) {
  event.target.style.color = 'red';
  event.target.style.fontSize = 34;
  let gauche = document.getElementById('gauche');
  gauche.style.backgroundColor = 'yellow';

  setTimeout(function() {
    event.target.style.color = '';
    gauche.style.backgroundColor = '';
    event.target.style.fontSize = 24;
  }, 2000);
}, false);

// Exercice 3
const killingRobot = {
  ref: 'KR-MACH001',
  codeName: 'Pedro',
  energySource: 'electricity',
  battery: {
    mAhCapacity: 1000000,
    material: 'adamantium',
    technology: 'high-power lithium-ion'
  },
  dimensions: {
    heightInCm: 450,
    widthInCm: 190,
    weightInKg: 3600
  },
  weaponry: [
    'laser beam machine guns',
    'nuclear rocket launchers',
    'adamantium sword',
    'adamantium spear',
    'H-Bomb',
    'electromagnetic impulse canon',
    'sulfuric acid high-pressure canon'
  ],
  tools: [
    'emergency self-repair nanotechnology',
    'advanced machine learning capabilities',
    'high capacity solar panels',
    'adamantium shell coating',
    'adamantium wings',
    'adamantium solar powered engines'
  ],
  abilities: {
    canWipeOutMankindFromTheFaceOfTheEarth: true,
    lovesAnimals: true,
    hasAchievedUltraInstinct: function() {
      if (this.battery.mAhCapacity >= 1000000) {
        alert('Adieu monde cruel!')
        return true;
      } else {
        return false;
      }
    },
    canFly: true,
    canSwim: false,
  },
};

// Exercice 4
function exercice4( arg1, arg2 ) {
  if (typeof arg1 === 'number' && typeof arg2 === 'number') {
    tmp = arg1 + arg2;
    return tmp * 3;
  }
  else if (typeof arg1 === 'string' && typeof arg2 === 'string') {
    tmp = arg1 + " " + arg2;
    return tmp;
  }
  else {
    return {
      'nombres': 'Il faut 2 nombres',
      'string': 'Il faut 2 chaine de caractère'
    }
  }
}

// Exercice 5
function exercice5 ( tab ) {
  let tmp = 0;
  for (let i = 0; i < tab.length; i++) {
    if (typeof tab[i] === 'number') {
      tmp = tmp + tab[i];
    }
  }
  return tmp;
} 