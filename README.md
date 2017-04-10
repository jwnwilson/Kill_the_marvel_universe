Kill the marvel universe Exercise

Plan of attack:

- (DONE) Build simple scraper with grequests for character API use comic IDs as that's all we need save data into characters.json (check comic ID limit doesn't break anything)

- (DONE) Write a simple reporter to output all characters alphabetically

- (DONE) Write simple reporter to output top 10 heros by comics

- (DONE) Build a networkx graph using comic IDs to connect heros in graph

- (DONE) Use networkx to calculate centrality and get top 10

- (DONE) Render graph to show character connections

- (DONE) Calculate influence based on similar logic from previous project using nx.neighbors to get basic
  influence of character and the surrounding characters to n levels - Looks like similar results to
  degree algorithm already implemented so will need to investigate graph to make sure it's built
  correctly

- After analysing the data, looks like the results could be correct but the amount of comic
  relations on each character is limited to 20 on initial API call I thought I checked this as per my
  notes, will have to go through characters for > 20 relations and make additional calls to get their extra relations

- Highlight high influence characters on graph and remove low influence to make it easier to digest

- Use community to work out the communities in the marvel universe and then find the most connected community bridges that will cover the most communities (Might be very similar to betweeness centrality already calculated)

- Show reasons for going for community links based on research that they are the ones who need to be vaccinated first inepidemics to fight them. 

- Clean up project finish tests and update coverage

- Add instructions on how to run crawler and different algorithms on data
