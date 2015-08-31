// 1 - Start enchant.js
enchant();
 
window.onload = function() {
    // Starting point
    var game = new Game($(window).width(), $(window).height());
    game.preload(	'assets/res/bg_pyranha.png', 
    							'assets/res/pyranha2.png', 
    							'assets/res/bubble_60.png',
    							'assets/res/plancton.png',
    							'assets/res/bgm.wav');
    game.fps = 30;
    game.scale = 1;
    game.onload = function() {
        // Once Game finish loading
        var scene = new SceneGame();
        game.pushScene(scene);
    }
    window.scrollTo(0,0);
    game.start();   
};



/**
 * SceneGame  
 */
var SceneGame = Class.create(Scene, {
    /**
     * The main gameplay scene.     
     */
    initialize: function() {
        var game, label, bg, penguin, iceGroup;
 
        // Call superclass constructor
        Scene.apply(this);
 
        // Access to the game singleton instance
        game = Game.instance;
 
        //Title label
				/*label = new Label("Pyranha");        
				label.x = ($(window).width() * 0.5) - (label.width * 0.5);
				label.y = 110;
				label.font = "110px 'Wire One',Helvetica,Arial,sans-serif";
				label.color = "#8CC84B";
				label.textAlign = "center";
        this.titleLabel = label;        */
 
        //Background
				bg = new Sprite($(window).width(), $(window).height());
				bg.image = game.assets['assets/res/bg_pyranha.png'];

        //Pyranha Logo

        pyranha = new Pyranha();
        pyranha.x = -115;
        pyranha.y = 130;
        this.penguin = pyranha;

        bubbleGroup = new Group();
        this.bubbleGroup = bubbleGroup;
 
        this.addChild(bg);
        this.addChild(bubbleGroup);
        this.addChild(pyranha);
        //this.addChild(label);

        this.addEventListener(Event.ENTER_FRAME,this.update);

        // Instance variables
        this.generateBubbleTimer = 0;
        this.generatePlanctonTimer = 0;
        
        this.bgm = game.assets['assets/res/bgm.wav']; // Add this line
 				//this.bgm.play();
    },

    
    update: function(evt) {
      
    	this.generateBubbleTimer += evt.elapsed * 0.001;
	    if(this.generateBubbleTimer >= 0.6)
	    {
    		var bubble;
        this.generateBubbleTimer -= 0.6;
        bubble = new Bubble(Math.floor(Math.random()*$(window).width()));
        this.bubbleGroup.addChild(bubble);
	    }

	    this.generatePlanctonTimer += evt.elapsed * 0.001;
	    if(this.generatePlanctonTimer >= 0.95)
	    {
    		var plancton;
        this.generatePlanctonTimer -= 0.95;
        plancton = new Plancton(Math.floor(Math.random()*$(window).width()));
        this.bubbleGroup.addChild(plancton);
	    }

	    
	    // Check collision
	    /*for (var i = this.iceGroup.childNodes.length - 1; i >= 0; i--) {
	        var ice;
	        ice = this.iceGroup.childNodes[i];
	        if(ice.intersect(this.penguin)){  
	            var game;
	            game = Game.instance;
	            game.assets['res/Hit.mp3'].play();                    
	            this.iceGroup.removeChild(ice);
	            this.bgm.stop();
	            game.replaceScene(new SceneGameOver(this.score));        
	            break;
	        }
	    }*/

	    // Loop BGM
	    /*if( this.bgm.currentTime >= this.bgm.duration ){
	        this.bgm.play();
	    }*/
    }
});

/**
 * Pyranha
 */
 var Pyranha = Class.create(Sprite, {
    initialize: function() {
      // Call superclass constructor
      Sprite.apply(this,[107, 88]);
      this.image = Game.instance.assets['assets/res/pyranha2.png'];
      this.animationDuration = 0;
      this.addEventListener(Event.ENTER_FRAME, this.update);
    },

    update: function (evt) {  

    	this.x = this.x + 1;
    	this.animationDuration += evt.elapsed * 0.001;       
        if(this.animationDuration >= 0.25)
        {
            this.frame = (this.frame + 1) % 2;
            this.animationDuration -= 0.25;
        }
    }
});


/**
 * Bubble
 */
var Bubble = Class.create(Sprite, {
    /**
     * The obstacle that the penguin must avoid
     */
    initialize: function(x_calc) {
        // Call superclass constructor
        Sprite.apply(this,[60, 60]);
        this.image  = Game.instance.assets['assets/res/bubble_60.png'];      
        this.rotationSpeed = 0;
        this.x = x_calc;
        this.y = $(window).height()+100;
        this.size_random = (Math.random()*0.6)+0.3;
        this.scale(this.size_random, this.size_random);
        this.addEventListener(Event.ENTER_FRAME, this.update);
    },

    update: function(evt) { 
    		var ySpeed, game;
     
        game = Game.instance;
        ySpeed = 20+(this.size_random*50);
     
        this.y -= ySpeed * evt.elapsed * 0.001;
        this.rotation += this.rotationSpeed * evt.elapsed * 0.001;           
        if(this.y < -100)
        {
            this.parentNode.removeChild(this);          
        }
    }
});


/**
 * Plancton
 */
var Plancton = Class.create(Sprite, {
    /**
     * The obstacle that the penguin must avoid
     */
    initialize: function(x_calc) {
        // Call superclass constructor
        Sprite.apply(this,[80, 75]);
        this.image  = Game.instance.assets['assets/res/plancton.png'];      
        this.rotationSpeed = 15;
        this.x = x_calc;
        this.y = $(window).height()+100;
        this.size_random = (Math.random()*0.4)+0.1;
        this.frame = Math.floor(Math.random() * 10);
        this.scale(this.size_random, this.size_random);
        this.addEventListener(Event.ENTER_FRAME, this.update);
    },

    update: function(evt) { 
    		var ySpeed, game;
     
        game = Game.instance;
        ySpeed = 20+(this.size_random*50);
     
        this.y -= ySpeed * evt.elapsed * 0.001;
        this.rotation += this.rotationSpeed * evt.elapsed * 0.001;           
        if(this.y < -100)
        {
            this.parentNode.removeChild(this);          
        }
    }
});




		
		
		

		

		