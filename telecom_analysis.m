% Data for all 10 states
states = {"Baja California", "Coahuila de Zaragoza", "Chihuahua", "Ciudad de México", "Guanajuato", "Jalisco", "Estado de México", "Nuevo León", "Sonora", "Veracruz de Ignacio de la Llave"};
years = 2015:2020;
technologies = {"Cable modem", "DSL", "Fiber optic", "Other technologies"};

% Data arrays for each state (2015-2020)
data = {
  [50 50 51 51 51 46; 44 40 37 34 28 23; 4 9 12 15 21 31; 2 1 1 0.1 0 0];
  [34 49 41 29 46 43; 55 43 49 57 40 32; 7 7 9 14 14 25; 4 2 1 0.5 0 0];
  [39 24 42 43 43 40; 52 56 39 36 29 23; 5 17 18 21 29 37; 3 2 1 0.3 0 0];
  [36 39 39 41 40 41; 39 31 27 24 20 15; 23 29 34 35 40 44; 2 1 1 0.2 0 0];
  [38 41 45 46 48 45; 53 47 42 39 35 30; 6 10 12 15 17 25; 3 2 1 0.3 0 0];
  [32 32 36 37 38 38; 53 46 40 37 33 29; 14 22 24 26 29 33; 1 1 0 0.1 0 0];
  [25 26 30 32 35 38; 64 58 50 46 39 28; 10 16 20 22 27 32; 0.4 0 0 0 0 0];
  [45 45 46 51 49 54; 34 30 25 23 19 15; 19 24 28 26 32 31; 3 1 1 0.3 0 0];
  [55 53 62 63 66 61; 41 40 32 30 27 25; 3 6 6 7 7 14; 1 0 0 0.1 0 0];
  [37 36 41 42 43 40; 58 56 50 46 42 37; 2 7 9 11 14 23; 2 1 0 0.1 0 0]
};

% Create a new figure
figure('Position', [100, 100, 1500, 1000]);

% Plot data for each state
for i = 1:10
  subplot(4, 3, i);
  bar(years, data{i}', 'stacked');
  title(states{i}, 'Interpreter', 'none');
  xlabel('Year');
  ylabel('Percentage');
  axis([2014.5, 2020.5, 0, 100]);
  grid on;
  if i == 10
    legend(technologies, 'Location', 'southoutside', 'Orientation', 'horizontal');
  end
end

% Adjust subplot layout
subplot(4, 3, 11, 'Visible', 'off');
subplot(4, 3, 12, 'Visible', 'off');

% Add main title
suptitle('Technology Adoption Trends in Mexican States (2015-2020)');

% Save the figure
print -dpng technology_trends_bar.png
