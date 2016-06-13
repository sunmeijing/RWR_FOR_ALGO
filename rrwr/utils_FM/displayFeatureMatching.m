function displayFeatureMatching(cdata, X, GT)

imgInput = appendimages( cdata.view(1).img, cdata.view(2).img );
imgInput = double(imgInput)./255;
imshow(rgb2gray(imgInput)); hold on;
iptsetpref('ImshowBorder','tight');

% draw false matches
curMatchList = cell2mat({cdata.matchInfo(:).match }');
idxFeat1 = curMatchList(:,1);
idxFeat2 = curMatchList(:,2);
feat1 = cdata.view(1).feat(idxFeat1,:);
feat2 = cdata.view(2).feat(idxFeat2,:);
feat2(:,1) = feat2(:,1) + size(cdata.view(1).img,2);
for i = 1:length(X)
    if X(i) && GT(i) == 0
        col1 = 'k';
        col2 = 'k';
    else
        continue;
    end
    plot([ feat1(i,1), feat2(i,1) ]...
    ,[ feat1(i,2), feat2(i,2) ],...
            '-','LineWidth',2,'MarkerSize',10,...
            'color', col1);

    drawellipse2( feat1(i,1:5), 1, 'k',4);
    drawellipse2( feat1(i,1:5), 1, col2,3);
    drawellipse2( feat2(i,1:5) ,1, 'k',4);
    drawellipse2( feat2(i,1:5) ,1, col2,3);                    
end
% draw true matches
for i = 1:length(X)
    if X(i) && GT(i) == 1
        col1 = 'y';
        col2 = 'y';
    else
        continue;
    end
    plot([ feat1(i,1), feat2(i,1) ]...
    ,[ feat1(i,2), feat2(i,2) ],...
            '-','LineWidth',5,'MarkerSize',10,...
            'color', 'k');
    plot([ feat1(i,1), feat2(i,1) ]...
    ,[ feat1(i,2), feat2(i,2) ],...
            '-','LineWidth',4,'MarkerSize',10,...
            'color', col1);

    drawellipse2( feat1(i,1:5), 1, 'k',5);
    drawellipse2( feat1(i,1:5), 1, col2,4);
    drawellipse2( feat2(i,1:5) ,1, 'k',5);
    drawellipse2( feat2(i,1:5) ,1, col2,4);                    
end                     

hold off