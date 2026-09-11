%% =========================================================
%  Drone Docking Analysis Script
%  Loads docking_trial_log.csv
%  Generates:
%   1. Drone Movement After Attachment
%   2. Docked Drone Drift Over Time
%   3. Movement Speed Over Time
%   4. 3D Attachment Point Motion
%
%  Also computes:
%   - max_drift
%   - avg_drift
%   - avg_speed
%   - max_speed
%
%  Save this as:
%     analyze_docking_trial.m
%
%  Run with:
%     analyze_docking_trial
%% =========================================================

clear;
clc;
close all;

%% =========================
%  USER SETTINGS
%% =========================

csv_file = '/home/harley-estrella/DroneDockingSim/trial_results/docking_trial_log.csv';

%% =========================
%  LOAD CSV
%% =========================

T = readtable(csv_file);

disp('CSV Loaded Successfully');
disp(head(T));

%% =========================
%  COMPUTE METRICS
%% =========================

max_drift = max(T.drift_from_original_m);

avg_drift = mean(T.drift_from_original_m);

avg_speed = mean(T.attach_point_speed_mps);

max_speed = max(T.attach_point_speed_mps);

%% =========================
%  PRINT RESULTS
%% =========================

fprintf('\n====================================\n');
fprintf('DOCKING TRIAL SUMMARY\n');
fprintf('====================================\n');

fprintf('Max Drift:      %.4f m\n', max_drift);
fprintf('Average Drift:  %.4f m\n', avg_drift);
fprintf('Average Speed:  %.4f m/s\n', avg_speed);
fprintf('Max Speed:      %.4f m/s\n', max_speed);

fprintf('====================================\n\n');

%% =========================================================
%  FIGURE 1
%  Drone Movement After Attachment
%% =========================================================

figure('Name','Drone Movement After Attachment');

plot(T.male_x, T.male_y, ...
    'LineWidth',2);

hold on;

plot(T.female_x, T.female_y, ...
    'LineWidth',2);

plot(T.attach_point_x, T.attach_point_y, ...
    'LineWidth',2);

xlabel('X Position (m)', 'FontSize', 12);
ylabel('Y Position (m)', 'FontSize', 12);

title('Drone Movement After Attachment', ...
    'FontSize', 16);

legend( ...
    'Male Drone', ...
    'Female Drone', ...
    'Attachment Point', ...
    'Location','best');

grid on;
axis equal;

saveas(gcf, 'figure1_drone_movement.png');

%% =========================================================
%  FIGURE 2
%  Docked Drone Drift Over Time
%% =========================================================

figure('Name','Docked Drone Drift Over Time');

plot( ...
    T.time_s, ...
    T.drift_from_original_m, ...
    'LineWidth',2);

xlabel('Time (s)', 'FontSize', 12);
ylabel('Drift (m)', 'FontSize', 12);

title('Docked Drone Drift Over Time', ...
    'FontSize', 16);

grid on;

saveas(gcf, 'figure2_drift_over_time.png');

%% =========================================================
%  FIGURE 3
%  Movement Speed Over Time
%% =========================================================

figure('Name','Movement Speed Over Time');

plot( ...
    T.time_s, ...
    T.attach_point_speed_mps, ...
    'LineWidth',2);

xlabel('Time (s)', 'FontSize', 12);
ylabel('Speed (m/s)', 'FontSize', 12);

title('Movement Speed Over Time', ...
    'FontSize', 16);

grid on;

saveas(gcf, 'figure3_speed_over_time.png');

%% =========================================================
%  FIGURE 4
%  3D Attachment Point Motion
%% =========================================================

figure('Name','3D Attachment Point Motion');

plot3( ...
    T.attach_point_x, ...
    T.attach_point_y, ...
    T.attach_point_z, ...
    'LineWidth',2);

xlabel('X Position (m)', 'FontSize', 12);
ylabel('Y Position (m)', 'FontSize', 12);
zlabel('Z Position (m)', 'FontSize', 12);

title('3D Attachment Point Motion', ...
    'FontSize', 16);

grid on;
axis equal;

saveas(gcf, 'figure4_3d_motion.png');

%% =========================
%  OPTIONAL COMBINED SUMMARY FIGURE
%% =========================

figure('Name','Summary Metrics');

subplot(2,2,1)
plot(T.male_x, T.male_y, 'LineWidth',2)
hold on
plot(T.female_x, T.female_y, 'LineWidth',2)
plot(T.attach_point_x, T.attach_point_y, 'LineWidth',2)
title('Movement')
grid on
axis equal

subplot(2,2,2)
plot(T.time_s, T.drift_from_original_m, 'LineWidth',2)
title('Drift')
grid on

subplot(2,2,3)
plot(T.time_s, T.attach_point_speed_mps, 'LineWidth',2)
title('Speed')
grid on

subplot(2,2,4)
plot3(T.attach_point_x, ...
      T.attach_point_y, ...
      T.attach_point_z, ...
      'LineWidth',2)
title('3D Motion')
grid on
axis equal

saveas(gcf, 'figure5_summary.png');

%% =========================
%  SAVE METRICS TO TEXT FILE
%% =========================

fid = fopen('trial_summary.txt', 'w');

fprintf(fid, 'DOCKING TRIAL SUMMARY\n');
fprintf(fid, '=====================\n\n');

fprintf(fid, 'Max Drift:      %.4f m\n', max_drift);
fprintf(fid, 'Average Drift:  %.4f m\n', avg_drift);
fprintf(fid, 'Average Speed:  %.4f m/s\n', avg_speed);
fprintf(fid, 'Max Speed:      %.4f m/s\n', max_speed);

fclose(fid);

disp('Summary text file saved.');
disp('All figures generated successfully.');

%% =========================
%  END
%% =========================