
function plot() {
  var width = window.innerWidth ;
  var height = window.innerHeight;
  
  var graph = d3.select("body")
      .append("div")
      .style("width", width + "px")
      .style("height", height + "px")
      .attr("id", "graph");

  var svg = graph  
      .append("svg")
      .attr("width", width)
      .attr("height", height);

      var attractForce = function() {
        var strength = 0.1;
        var nodes;
        var distances;
        var maxDistance = 100; 
        var mouse = [0, 0];
      
        function force(alpha) {
          nodes.forEach(function(d) {
            var dx = d.x - mouse[0];
            var dy = d.y - mouse[1];
            var distance = Math.sqrt(dx * dx + dy * dy);
            if(distance < distances[d.index] && distance < maxDistance) {
              d.vx -= (dx / distance) * (distances[d.index] - distance) * strength * alpha;
              d.vy -= (dy / distance) * (distances[d.index] - distance) * strength * alpha;
            }
          });
        }
        force.initialize = function(_) {
          nodes = _;
          distances = nodes.map(function(d) { return 100; });
        };
      
        force.mouse = function(_) {
          mouse = _ == null ? [0, 0] : _;
        };
      
        force.strength = function(_) {
          return arguments.length ? (strength = +_, force) : strength;
        };
      
        return force;
      };
      
      
      var myForce = attractForce().strength(0.1);

      var fdg = d3.forceSimulation()
    .force("link", d3.forceLink().distance(40).strength(.5))
    .force("center", d3.forceCenter(width / 2, height / 2 + 20))
    .force("charge", d3.forceManyBody().strength(-(height/20)))
    .force("attract", myForce)
    .force("x", d3.forceX(width/2).strength(0.1))
    .force("y", d3.forceY(height/2).strength(0.1))
    .alphaDecay(0.0005);
    
        svg.on("mousemove", function() {
            var point = d3.mouse(this);
            myForce.mouse(point);
            fdg.alphaTarget(0.9).restart();  
          });
          
            
    

    
    d3.json("https://raw.githubusercontent.com/MattTengtrakool/philenginedocs/main/phil.json", function(error, data) {
      if(error) throw error;
      
      var div = d3.select(".tooltip");
      
          var node = graph
              .attr("class", "nodes")
        .selectAll("img")
        .data(data.nodes)
        .enter().append("img")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
              .on("mouseover", function(d){
          div.transition()
            .duration(100)
            .style("opacity", 1);
          div.html('<span>'+d.country+'<span>');
          div.style("left",  (d3.event.pageX > (width - 200)) ? (d3.event.pageX - 130)+ "px":(d3.event.pageX + 30) + "px")
            .style("top", (d3.event.pageX > (width - 200)) ? (d3.event.pageY - 44) + "px":(d3.event.pageY - 30) + "px");
        })
              .on("mouseout", function(){
          div.transition()
            .duration(100)
            .style("opacity", 0)
          div
            .style("left", "-999px")
            .style("top", "-999px");
        })
        .attr("class", function(d){ return "node flag flag-" + d.code}  );
          
      var link = svg.append("g")
          .attr("class", "links")
        .selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("class", "link");
        
      fdg
        .nodes(data.nodes)
        .on('tick', tick);
      
      fdg.force("link")
        .links(data.links);
      function tick() {
        
              node
          .style("top", function(d) { return d.y + "px"; } )
          .style("left", function(d) { return d.x + "px"; });
              
        link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
        
        
      }
      
    
    });  
  
    
  function dragstarted(d) {
    if (!d3.event.active) fdg.alphaTarget(.5).restart();
     if (d3.event.x > 20 && d3.event.x < width -20)
    d.fx = d3.event.x;
    if (d3.event.y > 60 && d3.event.y < height-20)
    d.fy = d3.event.y;
  }
  
  function dragged(d) {
    if (d3.event.x > 20 && d3.event.x < width -20)
    d.fx = d3.event.x;
    if (d3.event.y > 60 && d3.event.y < height-20)
    d.fy = d3.event.y;
    
  }
  
  function dragended(d) {
    if (!d3.event.active) fdg.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
  
  addRandomCircles();
  
  }
  
  plot();
  
  function addRandomCircles() {
    for(var i = 0; i < 2000; i++) {
      var x = Math.random() * window.innerWidth,
          y = Math.random() * window.innerHeight;
      d3.select("svg")
        .append("circle")
        .attr("r", .7)
        .attr("class", "bkdCircles")
        .attr("fill", d3.interpolateWarm(Math.random()/2))
        .attr("cx", x)
        .attr("cy", y);
    }
  }
  