// http://stackoverflow.com/questions/7137860/javascript-namespace-declaration-with-function-prototype

var tau = 2 * Math.PI;
var quarter_tau = Math.PI / 2;

var VectorTwo = (function () {
	/** class Constructor **/
	var obj = function (x, y) {
		this.x = x;
		this.y = y;
	};
	
	/** class methods **/
	obj.prototype = {
		
		
		
	}
}

var BezierOne = (function () {
	/** class Constructor **/
	var obj = function (p0, p1, p2, p3) {
		this.ctrl = [p0, p1, p2, p3];
		this.start = 0.0;
		this.stop = 1.0;
	};
	/** class methods **/
	obj.prototype = {
		pos: function (t) {
			// return the position of the bezier curve as a function of t
		},
		spd: function (t) {
			// return the velocity of the bezier curve as a function of t
		}
	};
	return obj;
})();

var SimpleBrush = (function () {
	/* circular conic brush
	/** class Constructor **/
	var obj = function () {
		this.prev = null;
	};
	
	/** class methods **/
	obj.prototype = {
		drawTo: function (ctx, x, y, radius) {
			ctx.arc(x, y, radius, 0.0, tau, false);
			if (this.prev !== null) {
				var prev_radius = this.get_radius(this.prev.radius);
				let modulus = Math.sqrt(Math.pow(x - this.prev.x, 2) + Math.pow(y - this.prev.y, 2));
				if (max(radius, prev_radius) < modulus) {
					// alpha: angle between the two centers and the tangent
					let alpha = Math.acos((radius - prev_radius) / modulus);
					let argument = Math.atan2(x - prev.x, y - prev.y);
					ctx.moveTo(prev_radius * Math.cos(argument + alpha) + this.prev.x, prev_radius * Math.sin(argument + alpha) + this.prev.y);
					ctx.beginPath();
					ctx.lineTo(radius * Math.cos(argument + alpha) + x, radius * Math.sin(argument + alpha) + y);
					ctx.lineTo(radius * Math.cos(argument - alpha) + x, radius * Math.sin(argument - alpha) + y);
					ctx.lineTo(prev_radius * Math.cos(argument - alpha) + this.prev.x, prev_radius * Math.sin(argument - alpha) + this.prev.y);
					ctx.closePath();
				}
			}
			ctx.stroke();
			this.prev = {
				x: x,
				y: y,
				radius: radius
			};
		}
	}
})();

var Shodo3 = (function () {
	/** class Constructor **/
	var obj = function () {
		// x, y and z are N uni-dimensional curves, with a .pos() and a .spd() methods
		this.curve_lst = arguments;
	};
	
	/** class methods **/
	obj.prototype = {
		stroke: function(ctx) {
			
			
			
		}
